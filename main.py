import os
from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer   




data_ingestion = DataIngestion()
train_data_path, test_data_path = data_ingestion.initiate_data_ingestion()
print(train_data_path, test_data_path)

data_transformation=DataTransformation()
train_arr,test_arr,_=data_transformation.initiate_data_transformation(train_path=train_data_path,
                                                                        test_path=test_data_path)
print(train_arr, test_arr)
modeltrainer=ModelTrainer()
print(modeltrainer.initiate_model_trainer(train_arr,test_arr))