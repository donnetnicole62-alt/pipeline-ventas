"""Observabilidad: métricas en formato Prometheus (textfile collector)."""
import time
from pathlib import Path

from jobs.common import BASE_DIR

METRICS_FILE = BASE_DIR / "output" / "pipeline_metrics.prom"


def write_metrics(rows_in: int, rows_out: int, duration_s: float, success: bool) -> Path:
    ts = int(time.time())
    content = f"""# HELP pipeline_rows_input Registros leídos en la última corrida
# TYPE pipeline_rows_input gauge
pipeline_rows_input {rows_in}
# HELP pipeline_rows_output Registros escritos en la última corrida
# TYPE pipeline_rows_output gauge
pipeline_rows_output {rows_out}
# HELP pipeline_duration_seconds Duración de la última corrida
# TYPE pipeline_duration_seconds gauge
pipeline_duration_seconds {duration_s:.2f}
# HELP pipeline_last_run_success 1 si la última corrida terminó OK
# TYPE pipeline_last_run_success gauge
pipeline_last_run_success {1 if success else 0}
# HELP pipeline_last_run_timestamp Unix timestamp de la última corrida
# TYPE pipeline_last_run_timestamp gauge
pipeline_last_run_timestamp {ts}
"""
    METRICS_FILE.parent.mkdir(parents=True, exist_ok=True)
    METRICS_FILE.write_text(content)
    return METRICS_FILE
