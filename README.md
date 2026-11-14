# Observabilidade de Crédito — Pipeline de Validação, Drift e Governança

[![Python](https://img.shields.io/badge/Python-3.11-3776ab.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Pandera](https://img.shields.io/badge/Pandera-Data%20Contract-00A3E0.svg)](https://pandera.readthedocs.io/)
[![MLflow](https://img.shields.io/badge/MLflow-Tracking-0194e2.svg)](https://mlflow.org/)
[![Evidently](https://img.shields.io/badge/Evidently-AI-4A90E2.svg)](https://www.evidentlyai.com/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-ML-ff7f0e.svg)](https://scikit-learn.org/)
[![XGBoost](https://img.shields.io/badge/XGBoost-Classifier-2F8F2F.svg)](https://xgboost.ai/)

Este repositório implementa um pipeline end-to-end para validação de dados, treinamento de um modelo de risco de crédito, simulação de drift em produção, detecção estatística de degradação e observabilidade com MLflow. O projeto foi pensado para demonstrar como um modelo de crédito pode falhar silenciosamente quando a distribuição dos dados muda e como a governança, validação e monitoramento ajudam a reduzir esse risco.

---

## Índice

- [Objetivo do Projeto](#objetivo-do-projeto)
- [Contexto de Negócio](#contexto-de-negócio)
- [Arquitetura do Sistema](#arquitetura-do-sistema)
- [Estrutura do Repositório](#estrutura-do-repositório)
- [Requisitos](#requisitos)
- [Configuração do Ambiente](#configuração-do-ambiente)
- [Execução Passo a Passo](#execução-passo-a-passo)
- [Etapas do Projeto](#etapas-do-projeto)
- [Métricas e Critérios de Drift](#métricas-e-critérios-de-drift)
- [Observabilidade e Monitoramento](#observabilidade-e-monitoramento)
- [Governança, LGPD e Privacidade](#governança-lgpd-e-privacidade)
- [Vídeo STAR](#vídeo-star)
- [Como Contribuir](#como-contribuir)
- [Contato](#contato)

---

## Objetivo do Projeto

O objetivo principal do projeto é garantir que um modelo de risco de crédito continue confiável mesmo quando os dados de produção mudam ao longo do tempo. Para isso, o repositório implementa:

- validação estrita de dados antes da entrada no pipeline;
- treino de um classificador baseline para risco de crédito;
- simulação de cenários de produção com drift intencional;
- detecção estatística de mudança de distribuição (KS + PSI);
- geração de relatórios HTML para análise visual;
- observabilidade com MLflow e logs centralizados;
- documentação de governança e LGPD para privacidade e compliance.

Em outras palavras, o projeto mostra como evitar que “lixo” entre no modelo, como detectar degradação silenciosa e como registrar evidências operacionais para auditoria e governança.

---

## Contexto de Negócio

Modelos de crédito operam em ambientes que mudam constantemente. Mudanças no comportamento dos clientes, na renda, no nível de desemprego, em eventos macroeconômicos ou em padrões de resposta podem alterar a distribuição dos dados de entrada.

Quando isso acontece, o modelo pode continuar funcionando, mas com precisão e assertividade reduzidas. Em crédito, isso pode impactar diretamente decisões automatizadas, risco financeiro e conformidade regulatória.

Por isso, este projeto foi montado como uma solução de observabilidade e ML governance para risco de crédito, com foco em:

- prevenir ingestão de dados inválidos;
- monitorar degradação do modelo;
- documentar regras de qualidade e privacidade;
- criar rastreabilidade para auditoria e decisões.

---

## Arquitetura do Sistema

O fluxo principal do projeto é:

1. Carga do dataset de referência
2. Validação por contrato de dados (`Pandera`)
3. Treinamento do modelo baseline
4. Geração de dataset de produção com drift simulado
5. Previsão em produção
6. Comparação da referência com a produção
7. Cálculo de drift por KS e PSI
8. Geração de relatórios HTML
9. Registro em MLflow e logs do pipeline

Diagrama conceitual:

```text
Dataset de Referência
        ↓
Validação de Contrato (Pandera)
        ↓
Treino do Modelo Baseline (XGBoost + Pipeline)
        ↓
Dataset de Produção com Drift
        ↓
Previsão do Modelo
        ↓
Comparação Referência × Produção
        ↓
Detecção de Drift (KS + PSI)
        ↓
Relatórios HTML + MLflow + Logs
```

---

## Estrutura do Repositório

```text
observabilidade_credito/
├── README.md
├── PROJECT_SETUP.md
├── requirements.txt
├── dataset_referencia_credito.csv
├── data/
│   ├── train_reference.csv
│   ├── test_reference.csv
│   ├── dataset_production.csv
│   └── dataset_production_with_preds.csv
├── docs/
│   ├── OBSERVABILITY.md
│   └── PRIVACY_LGPD.md
├── logs/
│   └── pipeline.log
├── mlruns/
├── models/
│   └── baseline.pkl
├── reports/
│   ├── drift_report.html
│   ├── evidently_drift.html
│   └── assets/
├── scripts/
│   ├── demo_fail.py
│   └── generate_and_analyze_production.py
├── src/
│   ├── __init__.py
│   ├── contract.py
│   ├── data_processing.py
│   ├── drift_detection.py
│   ├── drift_simulation.py
│   ├── observability.py
│   ├── train_model.py
│   └── validate_and_train.py
└── .venv/
```

Descrição dos principais arquivos:

- `src/contract.py`: contrato de dados com regras rígidas
- `src/validate_and_train.py`: valida documento, divide treino/teste e treina baseline
- `src/train_model.py`: pipeline de treino + MLflow
- `src/drift_simulation.py`: geração do dataset de produção com drift
- `src/drift_detection.py`: KS + PSI + relatório HTML
- `scripts/generate_and_analyze_production.py`: orquestra geração de produção, scores e relatórios
- `src/observability.py`: logger central e registro no MLflow
- `docs/PRIVACY_LGPD.md`: plano de privacidade e LGPD
- `docs/OBSERVABILITY.md`: métricas de monitoramento e observabilidade

---

## Requisitos

### Requisitos do sistema

- Python 3.11
- Windows PowerShell ou terminal equivalente
- Acesso local para leitura e gravação de arquivos

### Dependências principais

O projeto utiliza as seguintes bibliotecas:

- `pandas`
- `numpy`
- `scikit-learn`
- `xgboost`
- `pandera`
- `mlflow`
- `evidently`
- `matplotlib`
- `seaborn`
- `scipy`

Todas as dependências estão listadas em `requirements.txt`.

---

## Configuração do Ambiente

### 1. Criar ambiente virtual

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2. Instalar dependências

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 3. Confirmar instalação

```powershell
python -m pip list
```

Se tudo estiver correto, o ambiente está pronto para execução.

---

## Execução Passo a Passo

### Passo 1 — Validar dataset de referência e treinar baseline

Execute:

```powershell
.venv\Scripts\python.exe -m src.validate_and_train
```

O que acontece:

- o arquivo `dataset_referencia_credito.csv` é carregado;
- a limpeza básica é aplicada;
- o contrato de dados é validado em `src/contract.py`;
- se houver erro de contrato, a execução falha imediatamente;
- os splits de treino e teste são salvos em `data/`;
- o modelo baseline é treinado e salvo em `models/baseline.pkl`;
- as métricas `roc_auc` e `accuracy` são calculadas.

Resultado esperado:

```text
Contrato OK — criando divisão treino/teste...
Treinamento concluído. Métricas: {'roc_auc': ..., 'accuracy': ...}
```

---

### Passo 2 — Demonstrar falha do contrato com batch inválido

Execute:

```powershell
.venv\Scripts\python.exe scripts\demo_fail.py
```

Esse script cria um lote intencionalmente ruim com:

- renda nula;
- duplicata em `SK_ID_CURR`;
- idade menor que 18 anos.

Resultado esperado:

```text
Falha esperada do contrato de dados:
ValueError: Contrato violado: há duplicatas em SK_ID_CURR.
```

Esse passo demonstra que o processo de ingestão está bloqueando lixo antes que o modelo receba dados inválidos.

---

### Passo 3 — Gerar dataset de produção com drift e gerar relatórios

Execute:

```powershell
.venv\Scripts\python.exe -c "import sys; sys.path.insert(0,'.'); from scripts import generate_and_analyze_production as g; g.main()"
```

O que acontece:

- o dataset de produção é gerado em `data/dataset_production.csv`;
- a distribuição de variáveis é modificada intencionalmente para simular drift;
- o modelo local é carregado e gera probabilidade de crédito;
- o dataset com previsões é salvo em `data/dataset_production_with_preds.csv`;
- o relatório customizado em `reports/drift_report.html` é salvo;
- o relatório Evidently em `reports/evidently_drift.html` também é salvo.

Resultado esperado:

```text
Dataset de produção gerado em data/dataset_production.csv
Dataset de produção pontuado e salvo em data\dataset_production_with_preds.csv
Relatório customizado de drift: reports\drift_report.html
Relatório Evidently salvo em reports\evidently_drift.html
```

---

### Passo 4 — Visualizar relatórios HTML

Abra os arquivos:

- `reports/drift_report.html`
- `reports/evidently_drift.html`

Esses relatórios mostram as variáveis que sofreram maior alteração de distribuição entre referência e produção.

---

### Passo 5 — Visualizar MLflow

No terminal, execute:

```powershell
.venv\Scripts\python.exe -m mlflow ui --backend-store-uri mlruns
```

Depois abra no navegador:

```text
http://localhost:5000
```

Você pode observar:

- experimento `baseline` com métricas do treinamento;
- experimento `monitoring` com métricas de drift e artefatos;
- artefatos do modelo e relatórios.

---

## Etapas do Projeto

### Etapa 1 — Validação de Dados e Contratos

Foco: garantir que lixo não entre no modelo.

Implementado com:

- `Pandera` como data contract
- regras estritas para idade, renda, duplicatas e valores nulos
- bloco de validação em `src/contract.py`
- execução em `src/validate_and_train.py`
- demonstração de falha em `scripts/demo_fail.py`

Regras do contrato:

- `SK_ID_CURR` obrigatório e sem duplicatas
- `AMT_INCOME_TOTAL` > 0
- `TARGET` deve ser 0 ou 1
- idade mínima de 18 anos
- ausência de valores nulos em campos críticos

---

### Etapa 2 — Simulação e Detecção de Drift

Foco: diagnosticar degradação do modelo ao longo do tempo.

Implementado com:

- `src/drift_simulation.py`
- `src/drift_detection.py`
- `scripts/generate_and_analyze_production.py`

A simulação de produção altera as distribuições das variáveis para representar uma mudança temporal realista. Em seguida, o projeto compara referência x produção usando:

- teste Kolmogorov-Smirnov (KS)
- Population Stability Index (PSI)
- Evidently AI para relatórios visuais

Critério utilizado:

- drift identificado quando `KS p-value < 0.05` ou `PSI > 0.1`

---

### Etapa 3 — Observabilidade de Pipelines e Modelos

Foco: monitorar saúde operacional do pipeline e do modelo.

Implementado com:

- `src/observability.py`
- `docs/OBSERVABILITY.md`
- MLflow para tracking e registro de artefatos
- logs em `logs/pipeline.log`

Métricas documentadas:

- status da execução do pipeline
- volume de dados processados
- latência
- número de features com drift
- quantidade de alertas
- top features de drift

---

### Etapa 4 — Governança

Foco: garantir conformidade e responsabilidade de dados.

Documentação disponível:

- `README.md` em seções de governança
- `docs/PRIVACY_LGPD.md`

Os documentos cobrem:

- tratamento de dados pessoais e identificadores;
- base legal para uso de dados em crédito;
- retenção, exclusão e anonimização;
- responsabilidade e procedimentos internos;
- necessidade de DPIA e explicabilidade.

---

## Métricas e Critérios de Drift

O projeto utiliza como referência os critérios mais comuns em monitoramento de ML:

- `KS` para comparar distribuições numéricas entre referência e produção;
- `PSI` para medir estabilidade de distribuição;
- visualização em HTML para análise de impacto;
- detecção de drift quando há mudança estatisticamente significativa.

Como os dados são simulados, o objetivo não é encontrar um modelo perfeito, mas demonstrar claramente que o drift pode acontecer e que ele deve ser detectado, reportado e governado.

---

## Observabilidade e Monitoramento

O projeto registra:

- logs de execução em `logs/pipeline.log`;
- métricas em MLflow;
- artefatos em `mlruns/`;
- relatórios HTML em `reports/`;
- status do pipeline e drift em experimentos do MLflow.

Para detalhamento completo da observabilidade, consulte:

- `docs/OBSERVABILITY.md`

---

## Governança, LGPD e Privacidade

O projeto adota uma abordagem de privacy by design e privacy by default. Isso significa que:

- dados sensíveis devem ser minimizados;
- identificadores diretos devem ser tratados com cuidado;
- o dataset de referência e o de produção devem ficar separados por propósito;
- logs e artefatos devem ser acessados de forma controlada;
- o uso de dados em decisões automatizadas exige documentação de base legal, governança e auditabilidade.

O projeto inclui também:

- plano de privacidade em `docs/PRIVACY_LGPD.md`;
- regras de retenção e eliminação de dados;
- documentação sobre explicabilidade e governança de decisões automatizadas;
- rastreio de artefatos por MLflow para auditoria.

---

## Vídeo STAR

A demonstração do projeto em formato STAR pode ser gravada e adicionada ao README com o link final do vídeo.

Exemplo de estrutura esperada:

- Situation: risco da degradação silenciosa de modelos de crédito no mundo real
- Task: validar dados, detectar drift e manter compliance
- Action: uso de Pandera, MLflow, Evidently e simulação de drift
- Result: relatório de drift apontando a degradação e alerta operacional

Link do vídeo:

```text
Adicionar link do vídeo final aqui
```

Exemplo de formato:

```text
https://youtu.be/SEU_VIDEO_AQUI
```

---

## Como Contribuir

1. Crie uma branch com uma mudança clara.
2. Mantenha o padrão de código e documentação em português do Brasil.
3. Execute os scripts principais antes de abrir PR.
4. Atualize a documentação quando houver mudança de comportamento.
5. Garanta que o projeto continua executável após as alterações.

---

## Contato

Projeto desenvolvido para fins acadêmicos e de demonstração de monitoramento e governança em modelos de risco de crédito.

Se quiser discutir melhorias, extensões ou ajustes de compliance, o ideal é manter o foco em:

- validação de dados;
- observabilidade;
- drift;
- privacidade e LGPD;
- rastreabilidade de modelos.

---

Para detalhes operacionais de observabilidade, consulte `docs/OBSERVABILITY.md`.
Para detalhes de privacidade e LGPD, consulte `docs/PRIVACY_LGPD.md`.
