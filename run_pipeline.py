"""Paso 6 - Script principal: ingesta -> validación -> transformación -> validación -> output."""
import sys
import time

from pyspark.sql import functions as F

from jobs.common import OUTPUT_PATH, get_logger, get_spark
from jobs.ingest import ingest
from jobs.metrics import write_metrics
from jobs.transform import transform
from jobs.validate import DataQualityError, validate_input, validate_output

log = get_logger("run_pipeline")


def main() -> int:
    start = time.time()
    spark = get_spark()
    rows_in = rows_out = 0
    try:
        df = ingest(spark)
        rows_in = df.count()
        validate_input(df)

        expected_total = df.agg(F.sum(F.col("cantidad") * F.col("precio_unitario"))).first()[0]
        result = transform(df)
        rows_out = result.count()
        validate_output(result, expected_total)

        result.write.mode("overwrite").parquet(str(OUTPUT_PATH))
        log.info("Output guardado en %s (Parquet)", OUTPUT_PATH)
        write_metrics(rows_in, rows_out, time.time() - start, True)
        log.info("PIPELINE OK en %.2fs", time.time() - start)
        return 0
    except DataQualityError:
        write_metrics(rows_in, rows_out, time.time() - start, False)
        log.exception("PIPELINE FALLÓ por calidad de datos")
        return 1
    finally:
        spark.stop()


if __name__ == "__main__":
    sys.exit(main())
