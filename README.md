#####################################################################
# Author: Mariusz Wieczorek                                         #
# Project: Data pipeline built using Airflow and Spark jobs         #
# Usage: This project is fully local environment where can be       #
#        processed hosts data                                       #
#####################################################################

To start this project and use it without any issues please follow by this hints below:
    1. Change paths related to project where imitations of paths are located:
          fix it by commit -done

    2. use invoke

        pip install invoke

        invoke -l

        invoke up - run containers

        airflow url: http://localhost:8080/
        admin/admin - user/pass

        airflow is running on local executor (!)

    3. to open parquet files there can be done in many ways - the most popular is to install hive locally and hadoop or cloud solutions s3 + athena etc. For this project gold layer
       is just processed by spark and show final dataframe in bash instead of build table with some NoSQL tools.

    4. docker
        check containers are runnig

        use invoke
        invoke -l

Glossary:

AIRFLOW - https://airflow.apache.org/ - Data pipeline orchestrator used to schedule tasks, very powerfull and scalable

PYSPARK - https://spark.apache.org/docs/latest/api/python/index.html - Distributed Dataset processing, in this project used locally

INVOKE - https://www.pyinvoke.org/ - very helpful to automate your daily tasks

DOCKER - https://www.docker.com/ - containerisation, in this project use docker-composer too

DATA LAKE - in this project is imitaion of file storage where we can process data using spark and save it to the environment like Redshift, Athena, Bigquery, hadoop etc. Only mention for idea, this project is using local file storage mounted to the airflow container.

MEDALION - medalion architecture in this project is data design pattern that organizes data into tiered layers (Bronze, Silver, and Gold) to progressively improve its quality and usability within a lakehouse


TODOS:
    code contains # TODO sections as an idea for improvement


WORK with DAGs/OPERATORS:
    Everytime new dag needs to be added then .py file should be moved to dags folder. Airflow authomatically add new DAG.
    The same with Operators.



