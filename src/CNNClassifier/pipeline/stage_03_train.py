import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from src.CNNClassifier.config import ConfigurationManager
from src.CNNClassifier.components.stage_03_train import Training
from src.CNNClassifier import logger
try:
    config = ConfigurationManager()
  
    training_config = config.get_training_config()
    training = Training(config=training_config)
    training.get_base_model()
    training.train_valid_generator()
    training.train()
    
except Exception as e:
    raise e