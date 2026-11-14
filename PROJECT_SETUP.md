# Configuração do Projeto

Este documento descreve como inicializar o ambiente de desenvolvimento local para o Tech Challenge - Fase 4.

Passos rápidos (Windows PowerShell):

1. Criar o ambiente virtual e instalar as dependências:

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install --upgrade pip
.venv\Scripts\python -m pip install -r requirements.txt
```

2. Executar comandos do projeto com o Python do ambiente virtual:

```powershell
.venv\Scripts\python -m pip list
```

Observações:
- Todo o desenvolvimento seguirá boas práticas: diretórios `src/`, `notebooks/` e `docs/`.
- Código, variáveis e comentários devem seguir o idioma português do Brasil.
- MLflow será usado localmente na pasta `mlruns/`.
