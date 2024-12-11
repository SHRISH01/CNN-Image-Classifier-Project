from CNNClassifier.utils.utils import read_yaml,create_directory
from CNNClassifier.entity.config_entity import DataIngestionConfig
from CNNClassifier.entity.config_entity import PrepareBaseModelConfig
from CNNClassifier.entity.config_entity import TrainingConfig
from CNNClassifier.entity.config_entity import EvaluationConfig
from CNNClassifier.constants import CONFIG_FILE_PATH, PARAMS_FILE_PATH
from pathlib import Path
import os

class ConfigurationManager:
    def __init__(
        self, 
        config_filepath = CONFIG_FILE_PATH,
        params_filepath = PARAMS_FILE_PATH):
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)
        create_directory([self.config.artifacts_root])
        
    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion
        
        create_directory([config.root_dir])
        
        data_ingestion_config =DataIngestionConfig(
            root_dir=config.root_dir,
            Source_URL=config.source_URL,
            local_data_file=config.local_data_file,
            unzip_dir=config.unzip_dir 
        )
        return data_ingestion_config

