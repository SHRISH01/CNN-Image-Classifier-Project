import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
import urllib.request as request
from zipfile import ZipFile
from src.CNNClassifier import logger
from pathlib import Path
from tqdm import tqdm
from src.CNNClassifier.entity import DataIngestionConfig
from src.CNNClassifier.utils import utils

class DataIngestion:
    def __init__(self,config:DataIngestionConfig):
        self.config=config

    def download_file(self):
        print(f"Debugging: source_url = {self.config.source_url}")
        print(f"Debugging: local_data_file = {self.config.local_data_file}")
        
        if not self.config.source_url or not self.config.source_url.startswith(("http://", "https://")):
            raise ValueError("Invalid or missing source URL.")
        
        request.urlretrieve(
            url=self.config.source_url,
            filename=self.config.local_data_file
        )
            

    def get_updated_list_of_files(self,list_of_files):
        return [f for f in list_of_files if f.endswith(".jpg")]

    def preprocess(self,zf,f,working_dir):
        target_filepath=os.path.join(working_dir,f)
        if not os.path.exists(target_filepath):
            zf.extract(f,working_dir)

    def unzip_and_clean(self):
        with ZipFile(file=self.config.local_data_file,mode="r") as zf:
                list_of_file=zf.namelist()
                updated_list_of_file=self.get_updated_list_of_files(list_of_file)
                for f in tqdm(updated_list_of_file):
                    self.preprocess(zf, f, self.config.unzip_dir)
