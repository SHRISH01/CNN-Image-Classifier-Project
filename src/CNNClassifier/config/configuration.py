
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from src.CNNClassifier.entity.config_entity import PrepareBaseModelConfig
from src.CNNClassifier.entity.config_entity import TrainingConfig
from src.CNNClassifier.entity.config_entity import EvaluationConfig
from src.CNNClassifier.utils.utils import read_yaml, create_directory
from src.CNNClassifier.entity.config_entity import DataIngestionConfig
from src.CNNClassifier import logger
from src.CNNClassifier.constants import CONFIG_FILE_PATH, PARAMS_FILE_PATH
from pathlib import Path
from typing import Any, Dict

class ConfigurationManager:
    def __init__(
        self, 
        config_filepath: Path = CONFIG_FILE_PATH,
        params_filepath: Path = PARAMS_FILE_PATH):
        """
        Initialize configuration manager
        
        Args:
            config_filepath (Path): Path to the configuration YAML file
            params_filepath (Path): Path to the parameters YAML file
        """
        try:
            self.config = read_yaml(config_filepath)
            self.params = read_yaml(params_filepath)
            
            # Ensure artifacts root directory is created
            create_directory([self.config.get('artifacts_root', 'artifacts')])
        except Exception as e:
            logger.error(f"Error initializing ConfigurationManager: {e}")
            raise
    
    def get_data_ingestion_config(self) -> DataIngestionConfig:
        """
        Get data ingestion configuration
        
        Returns:
            DataIngestionConfig: Configuration for data ingestion
        """
        try:
            # Safely access configuration with fallback
            config = self.config.get('data_ingestion', {})
            
            # Ensure root directory is created
            root_dir = config.get('root_dir', 'artifacts/data_ingestion')
            create_directory([root_dir])
            
            # Create and return DataIngestionConfig
            data_ingestion_config = DataIngestionConfig(
                root_dir=root_dir,
                source_url=config.get('source_url', ''),
                local_data_file=config.get('local_data_file', ''),
                unzip_dir=config.get('unzip_dir', '')
            )
            
            return data_ingestion_config
        
        except Exception as e:
            logger.error(f"Error in get_data_ingestion_config: {e}")
            raise
    
    def safe_get(self, config: Any, key: str, default: Any = None) -> Any:
        """
        Safely get a configuration value
        
        Args:
            config (Any): Configuration object or dictionary
            key (str): Key to retrieve
            default (Any, optional): Default value if key is not found
        
        Returns:
            Value of the key or default
        """
        try:
            return getattr(config, key, default)
        except AttributeError:
            return config.get(key, default) if isinstance(config, dict) else default
        
    def get_prepare_base_model_config(self) -> PrepareBaseModelConfig:
        config = self.config.prepare_base_model
        
        create_directory([config.root_dir])

        prepare_base_model_config = PrepareBaseModelConfig(
            root_dir=Path(config.root_dir),
            base_model_path=Path(config.base_model_path),
            updated_base_model_path=Path(config.updated_base_model_path),
            params_image_size=self.params.IMAGE_SIZE,
            params_learning_rate=self.params.LEARNING_RATE,
            params_include_top=self.params.INCLUDE_TOP,
            params_weights=self.params.WEIGHTS,
            params_classes=self.params.CLASSES
        )

        return prepare_base_model_config
    
    def get_training_config(self) -> TrainingConfig:
        training = self.config.training
        prepare_base_model = self.config.prepare_base_model
        params = self.params
        training_data = os.path.join(self.config.data_ingestion.unzip_dir, "PetImages")
        create_directory([Path(training.root_dir)])

        training_config = TrainingConfig(
            root_dir=Path(training.root_dir),
            trained_model_path=Path(training.trained_model_path),
            updated_base_model_path=Path(prepare_base_model.updated_base_model_path),
            training_data=Path(training_data),
            params_epochs=params.EPOCHS,
            params_batch_size=params.BATCH_SIZE,
            params_is_augmentation=params.AUGMENTATION,
            params_image_size=params.IMAGE_SIZE
        )
        return training_config 


    def get_validation_config(self) -> EvaluationConfig:
        eval_config = EvaluationConfig(
            path_of_model="artifacts/training/model.h5",
            training_data="artifacts/data_ingestion/PetImages",
            #all_params=self.params,
            params_image_size=self.params.IMAGE_SIZE,
            params_batch_size=self.params.BATCH_SIZE
        )
        return eval_config