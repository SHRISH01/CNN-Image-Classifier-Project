import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
import yaml
from src.CNNClassifier import logger
import json
from typing import Any
import joblib
from pathlib import Path
from ensure import ensure_annotations
from src.CNNClassifier.utils.box_manual import Box

@ensure_annotations
def read_yaml(path_to_yaml: Path) -> Box:
    with open(path_to_yaml) as yaml_file:
        content = yaml.safe_load(yaml_file)
        return Box(content)

@ensure_annotations
def save_json():
    pass

@ensure_annotations
def load_json():
    pass

@ensure_annotations
def save_model():
    pass

@ensure_annotations
def load_model():
    pass

@ensure_annotations
def get_size():
    pass

@ensure_annotations
def create_directory(path_to_directory:list,verbose=True):
    for path in path_to_directory:
        os.makedirs(path,exist_ok=True)
        if verbose:
            logger.info(f"create directory at : {path}")


