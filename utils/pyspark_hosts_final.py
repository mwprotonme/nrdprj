import os
import logging
from pyspark.sql import SparkSession

process_name = 'hosts_final'
logging.basicConfig()
logger = logging.getLogger(f'{process_name} processing')
logger.setLevel("INFO")


logger.info("Set env vars for spark")

spark = SparkSession.builder.appName("GoldLayerCreation").getOrCreate()

# Ścieżka bazowa
base_path = "/mnt/d/Mariusz/nord/data/silver/"

# Lista na znalezione pliki parquet
parquet_files = []

for root, dirs, files in os.walk(base_path):
    for file in files:
        if file.endswith(".parquet"):
            full_path = os.path.join(root, file)
            parquet_files.append(full_path)
            logger.info(f"parquet_files {parquet_files}")
df = None
for file_path in parquet_files:
    temp_df = spark.read.parquet(file_path).select('hosts')
    if df is None:
        df = temp_df  # pierwszy plik
    else:
        df = df.unionByName(temp_df)

df.write.mode("overwrite").parquet("file:///mnt/d/Mariusz/nord/data/gold/")

spark.stop()
