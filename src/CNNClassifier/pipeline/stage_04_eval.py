import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from src.CNNClassifier.config import ConfigurationManager
from src.CNNClassifier.components.stage_04_evaluate import Evaluation
from src.CNNClassifier import logger

try:
    config = ConfigurationManager()
    val_config = config.get_validation_config()
    evaluation = Evaluation(val_config)
    evaluation.evaluation()
    evaluation.save_score()
except Exception as e:
   raise e