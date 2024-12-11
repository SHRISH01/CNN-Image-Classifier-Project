import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from src.CNNClassifier.components.stage_01_data_ingestion import DataIngestion 
from src.CNNClassifier.components.stage_02_prepare_base_model import PrepareBaseModel
from src.CNNClassifier.components.stage_03_train import Training
from src.CNNClassifier.components.stage_04_evaluate import Evaluation