# Plano de Privacidade e LGPD

Este documento descreve o plano de privacidade e as medidas para conformidade com a LGPD (Lei Geral de Proteção de Dados), no contexto do projeto de risco de crédito.

- Dados pessoais minimizados: manter apenas colunas estritamente necessárias para o treinamento e a análise do modelo.
- Bases separadas: `dataset_referencia_credito.csv` (referência) e `data/dataset_production.csv` (produção simulada).
- Acesso local: todos os dados, logs e relatórios são armazenados localmente no repositório; não há transmissão para cloud.
- Registro de experimentos: MLflow armazena metadados em `mlruns/` localmente.
- Exclusão e anonimização: antes de qualquer exposição pública, remover identificadores diretos e considerar hashing ou anonimização.
- Finalidade: decisão de crédito e monitoramento de drift. A base legal adotada para o processamento é a execução de contrato e o legítimo interesse, conforme aplicável; registros de consentimento devem ser mantidos pelo controlador.

Retenção e anonimização:

- Dados pessoais identificáveis devem ser mantidos apenas pelo período estritamente necessário.
- Para compartilhamento ou publicação, gerar uma versão anonimizadas com hash ou remoção dos identificadores diretos.

Direitos dos titulares:

- Titulares podem solicitar acesso, correção, eliminação e portabilidade.
- Procedimentos de atendimento devem ser registrados no repositório de compliance da organização.

Responsável e contato:

- Responsável pelo projeto: equipe do desafio (preencher nome e e-mail de contato no sistema interno de compliance).

Observabilidade e auditoria:

- Logs de experimentos (MLflow) e relatórios de drift são mantidos localmente em `mlruns/` e `reports/` para auditoria interna.

