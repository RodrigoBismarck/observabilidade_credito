"""
Cria um dataset de produção com drift, faz previsões com o modelo local e gera relatórios de drift.

Execução:
  python -c "import sys; sys.path.insert(0,'.'); from scripts import generate_and_analyze_production as g; g.main()"

Saídas:
 - data/dataset_production.csv
 - data/dataset_production_with_preds.csv
 - reports/drift_report.html (customizado)
 - reports/evidently_drift.html (Evidently)
"""
from pathlib import Path
import sys

import pandas as pd

from src import drift_detection, drift_simulation, train_model
from src.observability import get_logger, log_pipeline_run


def score_model(model_path: str, df: pd.DataFrame, features=None):
    """Carrega o modelo local e retorna as probabilidades previstas para o DataFrame."""
    from joblib import load

    mdl = load(model_path)
    if features is None:
        features = [c for c in df.columns if c not in ['SK_ID_CURR', 'TARGET']]
    X = df[features]
    preds = mdl.predict_proba(X)[:, 1]
    return preds


def main(reference_csv: str = 'data/train_reference.csv'):
    """Executa o fluxo completo de produção com simulação de drift e análise estatística."""
    ref = Path(reference_csv)
    if not ref.exists():
        print('Treino de referência não encontrado — executando validação e treinamento para criar os splits e o modelo')
        sys.path.insert(0, '.')
        from src import validate_and_train

        validate_and_train.main()

    src_ref = 'dataset_referencia_credito.csv'
    prod_path = drift_simulation.create_and_save_production(src_ref, out_path='data/dataset_production.csv')
    print('Dataset de produção gerado em', prod_path)

    model_path = Path('models') / 'baseline.pkl'
    if not model_path.exists():
        print('Modelo local não encontrado — treinando modelo baseline para criá-lo')
        train_model.train_baseline('data/train_reference.csv', 'data/test_reference.csv')

    prod = pd.read_csv(prod_path)
    preds = score_model(str(model_path), prod)
    prod['PRED_PROB'] = preds
    out_preds = Path('data') / 'dataset_production_with_preds.csv'
    prod.to_csv(out_preds, index=False)
    print('Dataset de produção pontuado e salvo em', out_preds)

    drift_html, drift_results = drift_detection.detect_drift('data/train_reference.csv', str(out_preds), out_html='reports/drift_report.html')
    print('Relatório customizado de drift:', drift_html)

    logger = get_logger('generate_and_analyze_production')
    total = len(drift_results)
    drift_count = sum(1 for r in drift_results if (r['ks_pvalue'] < 0.05 or r['psi'] > 0.1))
    top = sorted(drift_results, key=lambda r: r['psi'], reverse=True)[:5]
    metrics = {'drift_total_features': total, 'drift_features_count': drift_count}
    for i, r in enumerate(top, start=1):
        metrics[f'top{i}_feature_psi'] = float(r['psi'])
        metrics[f'top{i}_feature_ks_pvalue'] = float(r['ks_pvalue'])

    artifacts = {
        'custom_drift_report': drift_html,
    }
    ev_path = Path('reports') / 'evidently_drift.html'
    if ev_path.exists():
        artifacts['evidently_report'] = str(ev_path)

    logger.info('Registrando execução de monitoramento no MLflow')
    log_pipeline_run(experiment_name='monitoring', run_name='drift_check', status='success', metrics=metrics, artifacts=artifacts)

    try:
        from evidently import Report
        from evidently.presets import DataDriftPreset

        ref_df = pd.read_csv('data/train_reference.csv')
        prod_df = pd.read_csv(str(out_preds))
        shared_cols = ref_df.columns.intersection(prod_df.columns).tolist()
        prod_df_filtered = prod_df[shared_cols]
        ref_df_filtered = ref_df[shared_cols]
        report = Report(metrics=[DataDriftPreset()])
        snapshot = report.run(reference_data=ref_df_filtered, current_data=prod_df_filtered)
        ev_out = Path('reports') / 'evidently_drift.html'
        ev_out.parent.mkdir(parents=True, exist_ok=True)
        snapshot.save_html(str(ev_out))
        print('Relatório Evidently salvo em', ev_out)
    except Exception as e:
        try:
            from evidently.dashboard import Dashboard
            from evidently.dashboard.tabs import DataDriftTab

            ref_df = pd.read_csv('data/train_reference.csv')
            prod_df = pd.read_csv(str(out_preds))
            dashboard = Dashboard(tabs=[DataDriftTab()])
            dashboard.calculate(ref_df, prod_df)
            ev_out = Path('reports') / 'evidently_drift.html'
            ev_out.parent.mkdir(parents=True, exist_ok=True)
            dashboard.save(str(ev_out))
            print('Dashboard Evidently salvo em', ev_out)
        except Exception as e2:
            print('Falha na geração do relatório Evidently:', e, ' / erro do fallback:', e2)


if __name__ == '__main__':
    main()
