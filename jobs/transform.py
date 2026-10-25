"""Paso 4 - Transformación: ingreso_total y agregación por fecha y producto."""
from pyspark.sql import DataFrame
from pyspark.sql import functions as F

from jobs.common import get_logger

log = get_logger("transform")


def add_ingreso_total(df: DataFrame) -> DataFrame:
    return df.withColumn("ingreso_total", F.col("cantidad") * F.col("precio_unitario"))


def aggregate_by_product_and_date(df: DataFrame) -> DataFrame:
    return (
        add_ingreso_total(df)
        .groupBy("fecha", "producto_id")
        .agg(F.round(F.sum("ingreso_total"), 2).alias("ingreso_total"))
        .orderBy("fecha", "producto_id")
    )


def transform(df: DataFrame) -> DataFrame:
    out = aggregate_by_product_and_date(df)
    log.info("Transformación OK: %d filas agregadas", out.count())
    return out
