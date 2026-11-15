"""
Contrato de dados para validação de lotes de referência e produção.

Regras rígidas:
- `SK_ID_CURR` deve ser único, obrigatório e preenchido
- `AMT_INCOME_TOTAL` deve ser maior que zero
- `TARGET` deve ser 0 ou 1
- `DAYS_BIRTH` deve indicar idade >= 18 anos
- registros duplicados devem bloquear a ingestão
"""
from __future__ import annotations

import pandas as pd
import pandera as pa
from pandera import Check, Column


def make_schema() -> pa.DataFrameSchema:
    """Cria o esquema do contrato de dados para o dataset de crédito."""
    schema = pa.DataFrameSchema(
        {
            "SK_ID_CURR": Column(pa.Int, checks=[Check(lambda s: s.notna())], nullable=False),
            "AMT_INCOME_TOTAL": Column(pa.Float, checks=[Check(lambda s: s.notna()), Check.gt(0)], nullable=False),
            "TARGET": Column(pa.Int, checks=[Check(lambda s: s.notna()), Check.isin([0, 1])], nullable=False),
            "CNT_CHILDREN": Column(pa.Float, checks=[Check(lambda s: s.notna()), Check.ge(0)], nullable=False),
            "DAYS_BIRTH": Column(pa.Int, checks=[Check(lambda s: s.notna())], nullable=False),
        },
        coerce=True,
    )
    return schema


def validate_contract(df: pd.DataFrame) -> pd.DataFrame:
    """Valida o dataframe contra o contrato e lança erro se falhar.

    Regras adicionais:
    - idade deve ser >= 18 anos
    - sem duplicatas de `SK_ID_CURR`
    - sem valores nulos nos campos críticos
    """
    schema = make_schema()

    if df.empty:
        raise ValueError('Contrato violado: o dataframe está vazio.')

    if 'SK_ID_CURR' not in df.columns:
        raise ValueError('Contrato violado: coluna `SK_ID_CURR` ausente.')

    if df['SK_ID_CURR'].duplicated().any():
        raise ValueError('Contrato violado: há duplicatas em SK_ID_CURR.')

    validated = schema.validate(df, lazy=True)

    if 'DAYS_BIRTH' in validated.columns:
        idade = (-validated['DAYS_BIRTH'] / 365.25).astype(int)
        if (idade < 18).any():
            raise ValueError('Contrato violado: existe registro com idade menor que 18 anos.')

    if validated['AMT_INCOME_TOTAL'].isna().any():
        raise ValueError('Contrato violado: há renda nula.')

    return validated
