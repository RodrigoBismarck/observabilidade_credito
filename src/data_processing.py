"""
Data loading and preprocessing utilities.

All comments in Portuguese. Public names and filenames in English.
"""
from pathlib import Path
import pandas as pd


def load_data(path: str) -> pd.DataFrame:
    """Carrega o CSV do caminho informado e retorna um DataFrame."""
    return pd.read_csv(path)


def basic_clean(df: pd.DataFrame) -> pd.DataFrame:
    """Limpeza mínima: remover linhas sem `SK_ID_CURR` e normalizar nomes.

    Comentários em português conforme requisito.
    """
    df = df.copy()
    df = df[~df['SK_ID_CURR'].isna()]
    # Garantir tipos básicos
    if 'TARGET' in df.columns:
        df['TARGET'] = df['TARGET'].astype(int)
    return df


def train_test_split_save(df: pd.DataFrame, out_dir: str = 'data', test_size: float = 0.2, random_state: int = 42):
    """Separa treino/teste e salva em CSV dentro de `out_dir`."""
    from sklearn.model_selection import train_test_split

    Path(out_dir).mkdir(parents=True, exist_ok=True)
    train, test = train_test_split(df, test_size=test_size, random_state=random_state, stratify=df.get('TARGET'))
    train_path = Path(out_dir) / 'train_reference.csv'
    test_path = Path(out_dir) / 'test_reference.csv'
    train.to_csv(train_path, index=False)
    test.to_csv(test_path, index=False)
    return str(train_path), str(test_path)


def save_production(df: pd.DataFrame, out_path: str):
    """Salva o dataset de produção (simulado) no caminho indicado."""
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)
    return out_path
