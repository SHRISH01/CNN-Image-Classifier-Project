import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from src.CNNClassifier.entity.config_entity import(DataIngestionConfig,
                                                   PrepareBaseModelConfig,
                                                   TrainingConfig,
                                                   EvaluationConfig)