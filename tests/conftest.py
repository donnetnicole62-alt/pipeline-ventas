import os
import sys

# Le dice a Spark que use el mismo Python que está corriendo los tests
os.environ.setdefault("PYSPARK_PYTHON", sys.executable)
os.environ.setdefault("PYSPARK_DRIVER_PYTHON", sys.executable)