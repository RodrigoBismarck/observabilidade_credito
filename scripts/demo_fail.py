"""
Demonstra a falha do contrato de dados ao criar um lote inválido e validar o batch.

Execução:
    python scripts/demo_fail.py

Este script deve imprimir a mensagem esperada de violação do contrato.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pandas as pd

from src import contract
from src.data_processing import basic_clean, load_data


def create_bad_batch(df: pd.DataFrame) -> pd.DataFrame:
    """Cria um batch intencionalmente inválido para testar o bloqueio do contrato."""
    bad = df.head(2).copy()

    bad.loc[0, 'AMT_INCOME_TOTAL'] = None
    bad.loc[1, 'SK_ID_CURR'] = bad.loc[0, 'SK_ID_CURR']

    if 'DAYS_BIRTH' in bad.columns:
        bad.loc[0, 'DAYS_BIRTH'] = -365 * 15

    return bad


def main():
    """Executa a validação em um lote inválido e imprime o erro esperando falha."""
    ref = Path('dataset_referencia_credito.csv')
    if not ref.exists():
        print('Dataset de referência não encontrado; não foi possível executar o demo_fail.')
        return

    df = load_data(str(ref))
    df = basic_clean(df)
    bad = create_bad_batch(df)

    print('Executando validação do contrato em lote intencionalmente inválido...')
    try:
        contract.validate_contract(bad)
        print('Erro inesperado: o lote inválido passou na validação.')
    except Exception as e:
        print('Falha esperada do contrato de dados:')
        print(type(e).__name__ + ':', e)


if __name__ == '__main__':
    main()
