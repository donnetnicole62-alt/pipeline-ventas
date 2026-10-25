"""Pruebas automatizadas: transformación, validaciones y pipeline end-to-end."""
import pytest
from pyspark.sql import SparkSession

from jobs.ingest import SCHEMA
from jobs.transform import add_ingreso_total, aggregate_by_product_and_date
from jobs.validate import DataQualityError, validate_input, validate_output


@pytest.fixture(scope="session")
def spark():
    s = (
        SparkSession.builder.master("local[1]")
        .appName("tests")
        .config("spark.ui.enabled", "false")
        .config("spark.sql.shuffle.partitions", "2")
        .getOrCreate()
    )
    yield s
    s.stop()


def make_df(spark, rows):
    from datetime import date

    data = [(date.fromisoformat(f), p, q, pr) for f, p, q, pr in rows]
    return spark.createDataFrame(data, SCHEMA)


# ---------- Transformación ----------
def test_ingreso_total_es_cantidad_por_precio(spark):
    df = make_df(spark, [("2023-01-01", 101, 20, 10.0)])
    row = add_ingreso_total(df).first()
    assert row["ingreso_total"] == 200.0


def test_agregacion_suma_por_fecha_y_producto(spark):
    df = make_df(
        spark,
        [
            ("2023-01-01", 101, 10, 10.0),
            ("2023-01-01", 101, 10, 10.0),  # mismo día/producto -> se suman
            ("2023-01-01", 102, 1, 5.0),
            ("2023-01-02", 101, 3, 10.0),
        ],
    )
    out = {(r["fecha"].isoformat(), r["producto_id"]): r["ingreso_total"]
           for r in aggregate_by_product_and_date(df).collect()}
    assert out[("2023-01-01", 101)] == 200.0
    assert out[("2023-01-01", 102)] == 5.0
    assert out[("2023-01-02", 101)] == 30.0
    assert len(out) == 3


# ---------- Validaciones ----------
def test_validate_input_ok(spark):
    df = make_df(spark, [("2023-01-01", 101, 1, 10.0)])
    assert validate_input(df)["nulos_en_columnas_clave"] == 0


def test_validate_input_detecta_cantidad_no_positiva(spark):
    df = make_df(spark, [("2023-01-01", 101, 0, 10.0)])
    with pytest.raises(DataQualityError):
        validate_input(df)


def test_validate_input_detecta_precio_negativo(spark):
    df = make_df(spark, [("2023-01-01", 101, 1, -5.0)])
    with pytest.raises(DataQualityError):
        validate_input(df)


def test_validate_input_detecta_nulos(spark):
    df = spark.createDataFrame([(None, 101, 1, 10.0)], SCHEMA)
    with pytest.raises(DataQualityError):
        validate_input(df)


def test_validate_output_detecta_total_distinto(spark):
    df = make_df(spark, [("2023-01-01", 101, 1, 10.0)])
    out = aggregate_by_product_and_date(df)
    with pytest.raises(DataQualityError):
        validate_output(out, expected_total=999.0)


# ---------- End-to-end ----------
def test_pipeline_end_to_end():
    """Corre el pipeline completo (debe ir último: main() cierra la SparkSession)."""
    import duckdb

    from jobs.common import DATA_PATH, OUTPUT_PATH
    from run_pipeline import main

    assert main() == 0

    n = duckdb.execute(f"select count(*) from read_parquet('{OUTPUT_PATH}/*.parquet')").fetchone()[0]
    assert n > 0
    total = duckdb.execute(
        f"select sum(ingreso_total) from read_parquet('{OUTPUT_PATH}/*.parquet')"
    ).fetchone()[0]
    src = duckdb.execute(
        f"select sum(cantidad*precio_unitario) from read_csv_auto('{DATA_PATH}')"
    ).fetchone()[0]
    assert abs(total - src) < 0.5
