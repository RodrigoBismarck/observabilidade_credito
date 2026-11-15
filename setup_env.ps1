# Script PowerShell para criar venv e instalar dependências (Windows)
python -m venv .venv
.venv\Scripts\python -m pip install --upgrade pip
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -m pip install "pandas<3.0"