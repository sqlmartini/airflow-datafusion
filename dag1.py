from pendulum import datetime
import os
from airflow.decorators import dag, task
from airflow.providers.microsoft.mssql.hooks.mssql import MsSqlHook
from airflow.providers.microsoft.mssql.operators.mssql import MsSqlOperator
from airflow.providers.google.cloud.operators.datafusion import CloudDataFusionStartPipelineOperator
from airflow.providers.google.cloud.operators.dataproc import DataprocCreateClusterOperator
from airflow.providers.google.cloud.operators.dataproc import DataprocDeleteClusterOperator

PROJECT_ID = os.environ['ENV_PROJECT_ID'] 
REGION = os.environ['ENV_DATAPROC_REGION']
INSTANCE_NAME = "data-fusion-prod-01"
PIPELINE_NAME = "test-config-pipeline_v2"
CDF_ENDPOINT = f"https://{INSTANCE_NAME}-{PROJECT_ID}-usc1.datafusion.googleusercontent.com/api"
SUBNET = "projects/anthonymm-477-2023062814323200/regions/us-central1/subnetworks/dataproc-serverless-subnet"

CLUSTER_CONFIG = {
    "master_config": {
        "num_instances": 1,
        "machine_type_uri": "n1-standard-4",
        "disk_config": {"boot_disk_type": "pd-standard", "boot_disk_size_gb": 1024},
    },
    "worker_config": {
        "num_instances": 2,
        "machine_type_uri": "n1-standard-4",
        "disk_config": {"boot_disk_type": "pd-standard", "boot_disk_size_gb": 1024},
    },
    "gce_cluster_config": {
        "subnetwork_uri": SUBNET,
    }
}
CLUSTER_NAME = "dag1"

@dag(
    start_date=datetime(2023, 1, 1), max_active_runs=3, schedule=None, catchup=False
)
def dag1():
    create_cluster = DataprocCreateClusterOperator(
        task_id="create_cluster",
        project_id=PROJECT_ID,
        cluster_config=CLUSTER_CONFIG,
        region=REGION,
        cluster_name=CLUSTER_NAME
    )

    @task
    def get_list_of_results():
        hook = MsSqlHook("mssql_default")
        results = hook.get_records("SELECT targetTableName, cdfProfile FROM config.Metadata2;")
        return results
    
    @task
    def create_params(result):
        targetTableName = result[0]
        cdfProfile = result[1]
        params = { 
                    'bq.datasetName' : 'adventureworks', 
                    'bq.tableName' : targetTableName,
                    'system.profile.name' : cdfProfile 
        }
        return params 

    all_params = create_params.expand(result=get_list_of_results())   

    run_cdf = CloudDataFusionStartPipelineOperator.partial(
        location=REGION,
        pipeline_name=PIPELINE_NAME,
        instance_name=INSTANCE_NAME,
        task_id="load_bq_from_source",
    ).expand(runtime_args=all_params)
    
    delete_cluster = DataprocDeleteClusterOperator(
        task_id="delete_cluster",
        project_id=PROJECT_ID,
        cluster_name=CLUSTER_NAME,
        region=REGION
    )

    create_cluster >> run_cdf >> delete_cluster

dag1()