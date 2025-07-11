from airflow import DAG
from datetime import datetime
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from operators.download_hosts_operator import DownloadHostsOperator
from airflow.operators.bash import BashOperator

default_args = {
    "start_date": datetime(2025, 7, 1),
}

DATASETS = ["stevenblack", "urlhaus", "1hosts-lite", "ad-wars"]

with DAG(
    dag_id="download_hosts_to_data_lake",
    default_args=default_args,
    schedule=None,
    catchup=False,
    tags=["hosts", "download"],
) as dag:
    spark_tasks = []
    for dataset in DATASETS:
        download_task = DownloadHostsOperator(
            task_id=f"download_{dataset}",
            dataset_name=dataset,
        )
        
        spark_task = BashOperator(
            task_id=f"run_pyspark_processing_{dataset}",
            bash_command=f"/opt/spark/bin/spark-submit --master local[*] /home/root/utils/pyspark_{dataset}_process.py",
            env={
                "JAVA_HOME": "/usr/lib/jvm/default-java",
                "AIRFLOW__LOGGING__ENABLE_TASK_LOG_MASKING": "False",
                "PYSPARK_HOME": "/opt/spark/bin"
            },
            dag=dag,
        )
        spark_tasks.append(spark_task)

        download_task >> spark_task
    
    spark_task_final = BashOperator(
            task_id=f"run_pyspark_final_gold",
            bash_command=f"/opt/spark/bin/spark-submit --master local[*] /home/root/utils/pyspark_hosts_final.py",
            env={
                "JAVA_HOME": "/usr/lib/jvm/default-java",
                "AIRFLOW__LOGGING__ENABLE_TASK_LOG_MASKING": "False",
                "PYSPARK_HOME": "/opt/spark/bin"
            },
            dag=dag,
        )
    spark_tasks >> spark_task_final

    spark_final_check = BashOperator(
            task_id=f"spark_final_check",
            bash_command=f"/opt/spark/bin/spark-submit --master local[*] /home/root/utils/pyspark_final_check.py",
            env={
                "JAVA_HOME": "/usr/lib/jvm/default-java",
                "AIRFLOW__LOGGING__ENABLE_TASK_LOG_MASKING": "False",
                "PYSPARK_HOME": "/opt/spark/bin"
            },
            dag=dag,
        )
    spark_task_final >> spark_final_check