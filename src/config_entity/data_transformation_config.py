import os
import sys

from dataclasses import dataclass

@dataclass
class DataTransformationConfig:
    train_data_path: str
    test_data_path: str 
    