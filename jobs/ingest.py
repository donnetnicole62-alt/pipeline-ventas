"""Paso 3 - Ingesta: lee el CSV con esquema explícito (evita inferencias frágiles)."""
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.types import DateType, DoubleType, IntegerType, StructField, StructType

from jobs.common import DATA_PATH, get_logger

log = get_logger("ingest")

SCHEMA = StructType(
    [
        StructField("fecha", DateType(), True),
        StructField("producto_id", IntegerType(), True),
        StructField("cantidad", IntegerType(), True),
        StructField("precio_unitario", DoubleType(), True),
    ]
)


def ingest(spark: SparkSession, path=DATA_PATH) -> DataFrame:
    df = spark.read.csv(str(path), header=True, schema=SCHEMA)
    n = df.count()
    log.info("Ingesta OK: %d registros leídos desde %s", n, path)
    return df
