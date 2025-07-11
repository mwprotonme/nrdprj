import os
import sys
import logging
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, regexp_replace, split

process_name = 'stevenblack'
logging.basicConfig()
logger = logging.getLogger(f'{process_name} processing')
logger.setLevel("INFO")


logger.info("Set env vars for spark")

#for local usage
#spark_home = "/usr/local/spark"
#java_home = "/usr/lib/jvm/java-11-openjdk-amd64"

#os.environ["SPARK_HOME"] = spark_home
#os.environ["JAVA_HOME"] = java_home
#os.environ["PYSPARK_PYTHON"] = "/usr/bin/python3"

#sys.path.insert(0, os.path.join(spark_home, "python"))
#sys.path.insert(0, os.path.join(spark_home, "python", "lib", "py4j-0.10.9.7-src.zip"))

logger.info("Create session for spark")
spark = SparkSession.builder.appName(f"Hosts loader {process_name}").master("local[*]").getOrCreate()

base_path = f"/home/root/data/stage/{process_name}"
logger.info(f"base_path set to {base_path}")

for root, dirs, files in os.walk(base_path):
    for file in files:
        full_path = os.path.join(root, file)
        logger.info(f"file to load is set to {full_path}")


df = spark.read.text('file:///' + os.path.abspath(full_path))

df_filtered = df.filter(~col("value").startswith("#"))

df_filtered = df_filtered.withColumn("hosts", split(col("value"), r"\s+").getItem(1))
df_filtered = df_filtered.select(df_filtered['hosts']).where('hosts is not null')

output_path = os.path.abspath(os.path.join("data/silver", f"{process_name}"))

logger.info(f"Saving to {output_path}")

if os.path.exists(output_path):
    logger.info(f"Target path exists")
    df_filtered.write.mode("overwrite").parquet('file:///' + output_path)
else:
    logger.info(f"Target path created {output_path}")
    os.makedirs(output_path)
    df_filtered.write.mode("overwrite").parquet('file:///' + output_path)