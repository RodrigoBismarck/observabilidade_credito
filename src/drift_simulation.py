"""
Simula um dataset de produção com drift de distribuição.
"""
from pathlib import Path

import numpy as np
import pandas as pd


def simulate_drift(df: pd.DataFrame, income_shift: float = 0.6, employed_add: int = 3000) -> pd.DataFrame:
    """Cria uma cópia do dataset com drift em `AMT_INCOME_TOTAL` e `DAYS_EMPLOYED`.

    - `income_shift` multiplica a renda para simular variação de distribuição
    - `employed_add` desloca os dias trabalhados para valores mais extremos
    """
    df2 = df.copy()
    if 'AMT_INCOME_TOTAL' in df2.columns:
        df2['AMT_INCOME_TOTAL'] = df2['AMT_INCOME_TOTAL'] * income_shift
    if 'DAYS_EMPLOYED' in df2.columns:
        df2['DAYS_EMPLOYED'] = df2['DAYS_EMPLOYED'] - employed_add
    return df2


def create_and_save_production(input_csv: str, out_path: str = 'data/dataset_production.csv') -> str:
    """Lê um dataset de entrada, aplica drift e salva a produção simulada."""
    df = pd.read_csv(input_csv)
    prod = simulate_drift(df)
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    prod.to_csv(out_path, index=False)
    return out_path


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default='dataset_referencia_credito.csv')
    parser.add_argument('--out', default='data/dataset_production.csv')
    args = parser.parse_args()
    out = create_and_save_production(args.input, args.out)
    print('Dataset de produção salvo em', out)
