"""
Valida o dataset de referência contra o contrato de dados e treina o modelo baseline.

Uso:
    python -m src.validate_and_train

Este script:
 - carrega `dataset_referencia_credito.csv` na raiz do projeto
 - aplica limpeza básica
 - valida o contrato em `src.contract`
 - separa treino/teste e salva em `data/`
 - treina o modelo baseline com `src.train_model.train_baseline`
"""
from pathlib import Path
import sys

import pandas as pd

from src import contract, train_model
from src.data_processing import basic_clean, load_data, train_test_split_save


def main(reference_csv: str = 'dataset_referencia_credito.csv'):
    if not Path(reference_csv).exists():
        print(f'Dataset de referência não encontrado: {reference_csv}')
        sys.exit(2)

    print('Carregando dataset de referência...')
    df = load_data(reference_csv)
    print('Aplicando limpeza básica...')
    df = basic_clean(df)

    print('Validando contrato de dados...')
    try:
        validated = contract.validate_contract(df)
    except Exception:
        print('Falha na validação do contrato de dados:')
        raise

    print('Contrato OK — criando divisão treino/teste...')
    train_path, test_path = train_test_split_save(validated, out_dir='data')
    print(f'Salvo treino -> {train_path} e teste -> {test_path}')

    print('Treinando modelo baseline...')
    resultado = train_model.train_baseline(train_path, test_path, experiment_name='baseline')
    print('Treinamento concluído. Métricas:', resultado)


if __name__ == '__main__':
    main()
