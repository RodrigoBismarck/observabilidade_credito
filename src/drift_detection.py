"""
Detecta drift de dados usando testes estatísticos (KS e PSI) e gera relatório em HTML.

A API do Evidently varia entre versões; aqui usamos testes estatísticos diretos
(KS e PSI) para garantir compatibilidade e produzir um relatório HTML robusto.
"""
from pathlib import Path
import base64
import io

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats


def psi(expected, actual, buckets=10):
    """Calcula o Population Stability Index entre duas distribuições."""
    def _to_breaks(arr, buckets):
        return np.percentile(arr, np.linspace(0, 100, buckets + 1))

    breaks = _to_breaks(expected, buckets)
    expected_perc = np.histogram(expected, bins=breaks)[0] / len(expected)
    actual_perc = np.histogram(actual, bins=breaks)[0] / len(actual)
    expected_perc = np.where(expected_perc == 0, 1e-6, expected_perc)
    actual_perc = np.where(actual_perc == 0, 1e-6, actual_perc)
    return np.sum((expected_perc - actual_perc) * np.log(expected_perc / actual_perc))


def detect_drift(reference_csv: str, production_csv: str, out_html: str = 'reports/drift_report.html'):
    """Compara dataset de referência e produção e gera relatório HTML de drift."""
    ref = pd.read_csv(reference_csv)
    prod = pd.read_csv(production_csv)
    Path(out_html).parent.mkdir(parents=True, exist_ok=True)

    numeric_cols = ref.select_dtypes(include=['int64', 'float64']).columns.tolist()
    results = []
    images = {}
    for col in numeric_cols:
        if col not in prod.columns:
            continue
        a = ref[col].dropna().values
        b = prod[col].dropna().values
        if len(a) < 10 or len(b) < 10:
            continue
        ks_stat, ks_p = stats.ks_2samp(a, b)
        psi_val = psi(a, b, buckets=10)
        results.append({'feature': col, 'ks_stat': float(ks_stat), 'ks_pvalue': float(ks_p), 'psi': float(psi_val)})

        plt.figure(figsize=(6, 3))
        plt.hist(a, bins=30, alpha=0.5, label='referência')
        plt.hist(b, bins=30, alpha=0.5, label='produção')
        plt.title(f'{col} - distribuição')
        plt.legend()
        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        images[col] = base64.b64encode(buf.read()).decode('utf-8')

    report_rel_assets = Path(out_html).parent / 'assets'
    css_path = 'assets/styles.css'
    js_path = 'assets/scripts.js'

    html = [
        '<!doctype html>',
        '<html><head><meta charset="utf-8"><title>Relatório de Drift</title>',
        f'<link rel="stylesheet" href="{css_path}">',
        '</head><body>'
    ]
    html.append('<h1>Relatório de Drift (KS & PSI)</h1>')

    total = len(results)
    drift_count = sum(1 for r in results if (r['ks_pvalue'] < 0.05 or r['psi'] > 0.1))
    html.append(f'<div class="summary"><div class="metrics"><div class="metric"><strong>Total de features:</strong> {total}</div><div class="metric"><strong>Features com drift:</strong> {drift_count}</div></div><div class="legend small">Legenda: linhas em vermelho indicam PSI acima de 0,1 ou p-valor KS menor que 0,05.</div></div>')

    drift_results = [r for r in results if (r['ks_pvalue'] < 0.05 or r['psi'] > 0.1)]
    html.append('<div class="controls"><button class="btn" onclick="showOnlyDrift()">Mostrar apenas drift</button><button class="btn secondary" onclick="showAllCards()">Mostrar todos</button><button class="btn secondary" onclick="exportTableCSV()">Baixar CSV</button><button class="btn secondary" onclick="toggleTable()">Alternar tabela completa</button></div>')

    html.append('<div class="card-grid" id="card-grid">')
    for r in drift_results:
        feat = r['feature']
        mean_ref = float(ref[feat].dropna().mean()) if feat in ref.columns else None
        mean_prod = float(prod[feat].dropna().mean()) if feat in prod.columns else None
        pct_change = None
        if mean_ref and mean_prod:
            try:
                pct_change = (mean_prod - mean_ref) / mean_ref * 100
            except Exception:
                pct_change = None
        img = images.get(feat)
        fid = feat.replace(' ', '_')
        html.append('<div class="card" data-drift="true">')
        html.append(f'<div class="title">{feat}</div>')
        html.append(f'<div class="stat">KS p-value: <strong>{r["ks_pvalue"]:.4g}</strong> &nbsp; PSI: <strong class="psi-high">{r["psi"]:.4f}</strong></div>')
        if mean_ref is not None and mean_prod is not None:
            html.append(f'<div class="small">Média referência: {mean_ref:.2f} — Média produção: {mean_prod:.2f} — Δ%: {pct_change:.1f}%</div>')
        if img:
            html.append(f'<div class="img-wrap img-{fid}"><img src="data:image/png;base64,{img}" style="max-width:320px"/></div>')
        html.append('</div>')
    html.append('</div>')

    html.append('<div class="card-grid" id="card-grid-all">')
    for r in results:
        feat = r['feature']
        if not (r['ks_pvalue'] < 0.05 or r['psi'] > 0.1):
            html.append(f'<div class="card" data-drift="false"><div class="title">{feat}</div><div class="small">KS p-value: {r["ks_pvalue"]:.4g} — PSI: {r["psi"]:.4f}</div></div>')
    html.append('</div>')

    html.append('<div id="all-table-wrap" class="hidden">')
    html.append('<table class="sortable" id="drift-table"><thead><tr><th>feature</th><th data-numeric="true">ks_stat</th><th data-numeric="true">ks_pvalue</th><th data-numeric="true">psi</th></tr></thead><tbody>')
    for r in results:
        is_drift = (r['ks_pvalue'] < 0.05 or r['psi'] > 0.1)
        row_class = 'drift' if is_drift else ''
        psi_class = 'psi-high' if r['psi'] > 0.1 else ''
        ks_class = 'ks-low' if r['ks_pvalue'] < 0.05 else ''
        html.append(f"<tr class=\"{row_class}\"><td>{r['feature']}</td><td>{r['ks_stat']:.4f}</td><td class=\"{ks_class}\">{r['ks_pvalue']:.4g}</td><td class=\"{psi_class}\">{r['psi']:.4f}</td></tr>")
    html.append('</tbody></table>')
    html.append('</div>')

    for col, img in images.items():
        fid = col.replace(' ', '_')
        html.append(f'<div class="feature-title"><h3>{col} <button class="toggle-btn toggle-images" data-for="{fid}">Mostrar imagens</button></h3></div>')
        html.append(f'<div class="img-wrap img-{fid} hidden"><img src="data:image/png;base64,{img}" style="max-width:900px;"/></div>')

    html.append(f'<script src="{js_path}"></script>')
    html.append('</body></html>')

    out = Path(out_html)
    report_rel_assets.mkdir(parents=True, exist_ok=True)
    out.write_text('\n'.join(html), encoding='utf-8')
    return str(out), results


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--ref', default='data/train_reference.csv')
    parser.add_argument('--prod', default='data/dataset_production.csv')
    parser.add_argument('--out', default='reports/drift_report.html')
    args = parser.parse_args()
    out, results = detect_drift(args.ref, args.prod, args.out)
    print('Relatório de drift salvo em', out)
    drifted = [r for r in results if (r['ks_pvalue'] < 0.05 or r['psi'] > 0.1)]
    print('Features com drift:', [d['feature'] for d in drifted])
