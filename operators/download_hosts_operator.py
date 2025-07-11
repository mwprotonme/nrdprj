from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
import os
import requests
import shutil
from urllib.parse import urlparse


DATASETS = {
    "stevenblack": "https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts",
    "urlhaus": "https://malware-filter.gitlab.io/malware-filter/urlhaus-filter-agh.txt",
    "1hosts-lite": "https://badmojr.gitlab.io/1hosts/Lite/adblock.txt",
    "ad-wars": "https://raw.githubusercontent.com/jdlingyu/ad-wars/master/hosts",
}

LOCAL_BASE_PATH = "/home/root/data/stage"

class DownloadHostsOperator(BaseOperator):
    template_fields = ("dataset_name",)

    @apply_defaults
    def __init__(self, dataset_name: str, **kwargs):
        super().__init__(**kwargs)
        self.dataset_name = dataset_name

    def execute(self, context):
        exec_date = context["execution_date"]
        self.log.info(f"execution_date from context: {exec_date}")
        url = DATASETS.get(self.dataset_name)

        if not url:
            raise ValueError(f"Dataset '{self.dataset_name}' not defined.")

        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path) or "hosts.txt"

        target_dir = os.path.join(LOCAL_BASE_PATH, self.dataset_name, str(exec_date.strftime("%Y-%m-%d")))
        target_path = os.path.join(target_dir, filename)
        self.log.info(f"target_dir = {target_dir}")
        self.log.info(f"target_path = {target_path}")

        response = requests.get(url)
        response.raise_for_status()
        
        if os.path.exists(target_dir):
            shutil.rmtree(target_dir)

        os.makedirs(target_dir)

        with open(target_path, "w", encoding="utf-8") as f:
            f.write(response.text)
        
        self.log.info(f"TARGET PATH = {target_path}")
        self.log.info(f"Downloaded file saved at {target_path}")