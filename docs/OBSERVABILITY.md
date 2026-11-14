**Métricas de observabilidade**

- **Status da execução do pipeline**: status do pipeline (sucesso/erro). Registrado como parâmetro do MLflow `status`.
- **Volume de dados**: quantidade de registros processados por execução. Registrado como métrica `data_volume`.
- **Latência**: tempo total da execução em segundos. Registrado como métrica `latency_seconds`.
- **Métricas de drift**:
  - `drift_total_features`: número de features numéricas avaliadas para drift.
  - `drift_features_count`: número de features sinalizadas como drifting (p-valor KS < 0,05 ou PSI > 0,1).
  - `topN_feature_psi` / `topN_feature_ks_pvalue`: PSI e p-valor KS das principais features.
- **Contagem de alertas**: número de alertas gerados por falhas ou drift crítico. Registrado como `alerts_count`.

Registro e armazenamento
- Os logs do pipeline ficam em `logs/pipeline.log`.
- Os relatórios de drift em HTML (custom + Evidently) ficam em `reports/` e também são salvos como artefatos do MLflow no experimento `monitoring`.

Como visualizar
- Use a interface do MLflow para consultar runs e métricas: `mlflow ui --backend-store-uri mlruns` e abra http://localhost:5000.
- Abra `reports/drift_report.html` ou `reports/evidently_drift.html` para verificar os relatórios visuais.

MLflow de observabilidade
------------------------

O rastreamento local do MLflow está habilitado no script de treinamento (`src/train_model.py`).

- Nome do experimento: `baseline` (definido via `mlflow.set_experiment`).
- Runs locais e artefatos ficam na pasta `mlruns/` na raiz do projeto.
- O modelo treinado é registrado como artefato do MLflow (`model`).

Para visualizar os runs localmente, execute:

```powershell
# na raiz do projeto
.venv\Scripts\mlflow ui
```

Observações:
- Artefatos do MLflow (modelos, parâmetros, métricas) não são enviados para o Git; ficam em `mlruns/`.
- O script de treinamento já registra as métricas `roc_auc` e `accuracy`.
