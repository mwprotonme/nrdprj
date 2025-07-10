import os
import sys
import logging
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, regexp_replace

process_name = 'final_check'
logging.basicConfig()
logger = logging.getLogger(f'{process_name} processing')
logger.setLevel("INFO")


logger.info("Set env vars for spark")

# for local usage
#spark_home = "/usr/local/spark"
#java_home = "/usr/lib/jvm/java-11-openjdk-amd64"

#os.environ["SPARK_HOME"] = spark_home
#os.environ["JAVA_HOME"] = java_home
#os.environ["PYSPARK_PYTHON"] = "/usr/bin/python3"

#sys.path.insert(0, os.path.join(spark_home, "python"))
#sys.path.insert(0, os.path.join(spark_home, "python", "lib", "py4j-0.10.9.7-src.zip"))

logger.info("Create session for spark")
spark = SparkSession.builder.appName(f"{process_name}").master("local[*]").getOrCreate()

base_path = f"/mnt/d/Mariusz/nord/data/gold/"
logger.info(f"base_path set to {base_path}")
parquet_files = []

for root, dirs, files in os.walk(base_path):
    for file in files:
        if file.endswith(".parquet"):
            full_path = os.path.join(root, file)
            logger.info(f"parquet_files {full_path}")

print(f'full_path {full_path}')
final_df = spark.read.parquet(full_path)


logger.info(f"SHOW!!!!")
final_df.show()
