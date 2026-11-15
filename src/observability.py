"""Helpers de observabilidade: logger central e utilitários do MLflow.

Fornece:
- `get_logger()` retorna um logger configurado para escrever em `logs/pipeline.log`.
- `log_pipeline_run()` registra status, métricas e artefatos do pipeline no MLflow.
"""
import logging
from pathlib import Path
from typing import Dict

import mlflow


def _reset_malformed_mlflow_experiments(root: Path = None) -> None:
    """Remove pastas de experimentos corrompidos do MLflow para evitar warnings no setup da primeira execucao."""
    if root is None:
        root = Path('mlruns')

    if not root.exists():
        return

    for child in list(root.iterdir()):
        if child.is_dir() and child.name.isdigit():
            meta = child / 'meta.yaml'
            if not meta.exists():
                try:
                    for nested in sorted(child.iterdir(), reverse=True):
                        if nested.is_dir() or nested.is_file():
                            # remove artefatos quebrados de experimentos antigos
                            if nested.is_dir():
                                import shutil
                                shutil.rmtree(nested)
                            else:
                                nested.unlink()
                    child.rmdir()
                except Exception:
                    pass


def get_logger(name: str = 'observabilidade') -> logging.Logger:
    logs_dir = Path('logs')
    logs_dir.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        fh = logging.FileHandler(logs_dir / 'pipeline.log')
        fmt = logging.Formatter('%(asctime)s %(levelname)s %(name)s: %(message)s')
        fh.setFormatter(fmt)
        logger.addHandler(fh)
    return logger


def log_pipeline_run(experiment_name: str, run_name: str, status: str, metrics: Dict[str, float] = None, artifacts: Dict[str, str] = None):
    """"Inicia uma execução do MLflow para registrar status, métricas e artefatos do pipeline.

    - `status`: por exemplo, 'success' ou 'failure'
    - `metrics`: dicionário com métricas escalares para registrar
    - `artifacts`: dicionário com nome_do_artefato -> caminho para registrar
    """
    _reset_malformed_mlflow_experiments()
    mlflow.set_experiment(experiment_name)
    with mlflow.start_run(run_name=run_name):
        mlflow.log_param('status', status)
        if metrics:
            for k, v in metrics.items():
                try:
                    mlflow.log_metric(k, float(v))
                except Exception:
                    pass
        if artifacts:
            for name, path in artifacts.items():
                try:
                    mlflow.log_artifact(path, artifact_path=name)
                except Exception:
                    pass
