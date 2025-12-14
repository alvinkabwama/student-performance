import os
import sys

import numpy as np 
import pandas as pd
import pickle
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

from src.exception.exception import CustomException

def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)

    except Exception as e:
        raise CustomException(e, sys)
    
def evaluate_models(X_train, y_train, X_test, y_test, models, param):
    try:
        report = {}

        total_models = len(models)
        print(f"Starting model evaluation for {total_models} models\n")

        for i in range(len(list(models))):
            model_name = list(models.keys())[i]
            model = list(models.values())[i]
            para = param[model_name]

            print(f"[{i+1}/{total_models}] Training model: {model_name}")

            try:
                print(f"  -> Running GridSearchCV for {model_name}")
                gs = GridSearchCV(model, para, cv=3)
                gs.fit(X_train, y_train)

                print(f"  -> Best params found: {gs.best_params_}")
                model.set_params(**gs.best_params_)
                model.fit(X_train, y_train)

            except Exception as e:
                print(f"  -> GridSearch failed for {model_name}, training with default params")
                model.fit(X_train, y_train)

            y_test_pred = model.predict(X_test)
            test_model_score = r2_score(y_test, y_test_pred)

            print(f"  -> {model_name} test R2 score: {test_model_score:.4f}\n")

            report[model_name] = test_model_score

        print("Model evaluation completed\n")
        return report

    except Exception as e:
        raise CustomException(e, sys)

    
def load_object(file_path):
    try:
        with open(file_path, "rb") as file_obj:
            return pickle.load(file_obj)

    except Exception as e:
        raise CustomException(e, sys)
