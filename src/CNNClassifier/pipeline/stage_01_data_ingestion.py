import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from src.CNNClassifier.components.stage_01_data_ingestion import DataIngestion
from src.CNNClassifier.config.configuration import ConfigurationManager
from src.CNNClassifier import logger



logger.info(f"data ingesiton stage started")

config = ConfigurationManager()
data_ingestion_config = config.get_data_ingestion_config()
data_ingestion = DataIngestion(config=data_ingestion_config)
data_ingestion.download_file()
data_ingestion.unzip_and_clean()

logger.info(f"data ingesiton stage completed")