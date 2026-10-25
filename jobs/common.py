"""Utilidades compartidas: logging estructurado y creación de SparkSession."""
import logging
import os
from pathlib import Path

from pyspark.sql import SparkSession

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "ventas.csv"
OUTPUT_PATH = BASE_DIR / "output" / "ingresos_por_producto_fecha"


def get_logger(name: str) -> logging.Logger:
    logging.basicConfig(
        level=os.getenv("LOG_LEVEL", "INFO"),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
    return logging.getLogger(name)


def get_spark(app_name: str = "ventas_pipeline") -> SparkSession:
    spark = (
        SparkSession.builder.appName(app_name)
        .master(os.getenv("SPARK_MASTER", "local[2]"))
        .config("spark.ui.showConsoleProgress", "false")
        .config("spark.sql.shuffle.partitions", "4")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("ERROR")
    return spark
