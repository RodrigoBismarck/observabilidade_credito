# Script para executar pipeline completo: validar contrato, separar dados, treinar, simular drift, detectar drift

Write-Output "1) Carregar e limpar dados"
.venv\Scripts\python -c "from src.data_processing import load_data,basic_clean,train_test_split_save; import pandas as pd; df=load_data('dataset_referencia_credito.csv'); df=basic_clean(df); train_path,test_path=train_test_split_save(df,out_dir='data'); print('Saved:',train_path, test_path)"

Write-Output "2) Validar contrato de dados (pandera)"
.venv\Scripts\python -c "from src.contract import validate_contract; import pandas as pd; df=pd.read_csv('data/train_reference.csv'); validate_contract(df); print('Contract validation passed')"

Write-Output "3) Treinar baseline e registrar no MLflow"
.venv\Scripts\python -m src.train_model --train data/train_reference.csv --test data/test_reference.csv

Write-Output "4) Simular dataset de produção com drift"
.venv\Scripts\python -m src.drift_simulation --input data/train_reference.csv --out data/dataset_production.csv

Write-Output "5) Detectar drift e gerar relatório"
.venv\Scripts\python -m src.drift_detection --ref data/train_reference.csv --prod data/dataset_production.csv --out reports/drift_report.html

Write-Output "Pipeline concluído. Relatório em reports/drift_report.html"
