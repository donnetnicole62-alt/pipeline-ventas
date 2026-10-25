"""Paso 7 - Validación de datos. Falla el pipeline si algo está mal."""
from pyspark.sql import DataFrame
from pyspark.sql import functions as F

from jobs.common import get_logger

log = get_logger("validate")


class DataQualityError(Exception):
    pass


def validate_input(df: DataFrame) -> dict:
    """Valida el dataset crudo (antes de transformar)."""
    key_cols = ["fecha", "producto_id", "cantidad", "precio_unitario"]
    nulls = df.filter(F.greatest(*[F.col(c).isNull().cast("int") for c in key_cols]) == 1).count()
    non_positive_qty = df.filter(F.col("cantidad") <= 0).count()
    negative_price = df.filter(F.col("precio_unitario") < 0).count()
    results = {
        "nulos_en_columnas_clave": nulls,
        "cantidad_no_positiva": non_positive_qty,
        "precio_negativo": negative_price,
    }
    failed = {k: v for k, v in results.items() if v > 0}
    if failed:
        log.error("Validación de entrada FALLÓ: %s", failed)
        raise DataQualityError(f"Validación de entrada fallida: {failed}")
    log.info("Validación de entrada OK: %s", results)
    return results


def validate_output(df: DataFrame, expected_total: float) -> dict:
    """Valida el output: sin negativos, sin nulos y que conserve el total de ingresos."""
    negatives = df.filter(F.col("ingreso_total") < 0).count()
    nulls = df.filter(F.col("ingreso_total").isNull()).count()
    duplicates = df.count() - df.dropDuplicates(["fecha", "producto_id"]).count()
    total = df.agg(F.sum("ingreso_total")).first()[0]
    total_ok = abs(total - expected_total) < 0.01 * max(1, df.count())  # tolerancia por redondeo
    results = {
        "ingresos_negativos": negatives,
        "ingresos_nulos": nulls,
        "claves_duplicadas": duplicates,
        "total_conservado": bool(total_ok),
    }
    if negatives or nulls or duplicates or not total_ok:
        log.error("Validación de salida FALLÓ: %s", results)
        raise DataQualityError(f"Validación de salida fallida: {results}")
    log.info("Validación de salida OK: %s", results)
    return results
