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

def create_directory(paths):
    for path in paths:
        path = Path(path)  # Convert string to Path if needed
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
 
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
            # Print out the entire configuration to check its structure
            print("Config Loaded:", self.config)
            
            # Check if 'prepare_base_model' is in the configuration
            prepare_base_model_config = self.config.get('prepare_base_model')
            
            if prepare_base_model_config is None:
                # If not in config, try accessing through data_ingestion
                prepare_base_model_config = self.config.get('data_ingestion', {}).get('prepare_base_model')
            
            if prepare_base_model_config is None:
                raise ValueError("Missing 'prepare_base_model' configuration in both 'prepare_base_model' and 'data_ingestion' keys.")
            
            create_directory([Path(prepare_base_model_config.get('root_dir'))])
            
            return PrepareBaseModelConfig(
                root_dir=Path(prepare_base_model_config.get('root_dir')),
                base_model_path=Path(prepare_base_model_config.get('base_model_path')),
                updated_base_model_path=Path(prepare_base_model_config.get('updated_base_model_path')),
                params_image_size=self.params.IMAGE_SIZE,
                params_learning_rate=self.params.LEARNING_RATE,
                params_include_top=self.params.INCLUDE_TOP,
                params_weights=self.params.WEIGHTS,
                params_classes=self.params.CLASSES
            )



    
    def get_training_config(self) -> TrainingConfig:
        # Debug print to check the configuration
        print("Full Config:", self.config)
        
        # Safely retrieve configuration sections
        training = self.config.get('training', {})
        data_ingestion = self.config.get('data_ingestion', {})
        
        # Explicitly try to get prepare_base_model configuration
        prepare_base_model = (
            data_ingestion.get('prepare_base_model') or 
            self.config.get('prepare_base_model') or 
            {}
        )
        
        params = self.params
        
        # Construct training data path
        training_data = os.path.join(data_ingestion.get('unzip_dir', ''), "PetImages")
        
        # Ensure root directory exists
        create_directory([Path(training.get('root_dir', 'artifacts/training'))])

        # Safely access paths with fallbacks
        training_config = TrainingConfig(
            root_dir=Path(training.get('root_dir', 'artifacts/training')),
            trained_model_path=Path(training.get('trained_model_path', 'artifacts/training/model.h5')),
            updated_base_model_path=Path(prepare_base_model.get('updated_base_model_path', 'artifacts/prepare_base_model/base_model_updated.h5')),
            training_data=Path(training_data),
            params_epochs=params.get('EPOCHS', 1),
            params_batch_size=params.get('BATCH_SIZE', 32),
            params_is_augmentation=params.get('AUGMENTATION', False),
            params_image_size=params.get('IMAGE_SIZE', (224, 224))
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