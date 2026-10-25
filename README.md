# Pipeline de Ventas (end-to-end)

Pipeline de datos que ingesta ventas, calcula el ingreso por producto y fecha con PySpark, valida la calidad, guarda en Parquet y expone métricas. Incluye modelos dbt, DAG de Airflow, Docker, CI/CD y observabilidad (Prometheus + Grafana).

## 1. Descripción
Transforma ventas crudas (`fecha, producto_id, cantidad, precio_unitario`) en un dataset agregado `ingreso_total` por `fecha` y `producto_id`, listo para análisis o dashboards.

## 2. Dataset
`data/ventas.csv` (500 filas sintéticas, seed fija; se regenera con `python data/generate_data.py`).

| columna | tipo | descripción |
|---|---|---|
| fecha | date | día de la venta (enero 2023) |
| producto_id | int | 101–105 |
| cantidad | int | unidades (1–20) |
| precio_unitario | double | precio por unidad |

## 3. Cómo ejecutar
```bash
pip install -r requirements.txt     # requiere Java 17+ para PySpark
python data/generate_data.py        # genera el dataset
python run_pipeline.py              # ingesta -> validación -> transformación -> validación -> Parquet
python -m pytest -v                 # tests
cd dbt_project && dbt run --profiles-dir . && dbt test --profiles-dir .
# o todo junto: make all
# con Docker: docker compose up --build
```

## 4. Resultado esperado
- `output/ingresos_por_producto_fecha/` — Parquet con 148 filas (`fecha, producto_id, ingreso_total`).
- `output/pipeline_metrics.prom` — métricas Prometheus de la corrida.
- `output/warehouse.duckdb` — tablas dbt (mismo resultado, cruzable con PySpark).

## 5. Decisiones técnicas
- **PySpark** (y no solo pandas): demuestra procesamiento distribuido; el mismo código escala a un cluster cambiando `SPARK_MASTER`.
- **Parquet**: formato columnar, comprimido y con esquema; ideal para analítica.
- **Esquema explícito** en la lectura: evita inferencias frágiles y falla temprano si cambia el formato.
- **Validaciones en entrada y salida**: el pipeline corta (exit code 1) ante datos inválidos.
- **dbt + DuckDB**: capa SQL declarativa con tests, sirve de verificación cruzada del resultado de Spark.

## Estructura
```
data/  jobs/  tests/  output/  dags/  dbt_project/  observability/  .github/workflows/
run_pipeline.py  Dockerfile  docker-compose.yml  Makefile
```
