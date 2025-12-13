import os
import sys

# Custom exception class used to wrap and enrich exceptions
# with file name and line number information
from src.exception.exception import CustomException

# Centralized logger utility that ensures logging is configured once
# and returns a module-specific logger
from src.logging.logger import get_logger

# Configuration dataclass holding paths and parameters
# required for the data ingestion step
from src.config_entity.data_ingestion_config import DataIngestionConfig

# Configuration dataclass used later by the data transformation step
from src.config_entity.data_transformation_config import DataTransformationConfig

import pandas as pd
from sklearn.model_selection import train_test_split

# Create a logger specific to this module.
# __name__ ensures logs are traceable to this file.
logger = get_logger(__name__)


class DataIngestion:
    """
    DataIngestion is responsible for:
    - Reading raw data from the source
    - Persisting raw data
    - Splitting data into train and test sets
    - Saving train and test datasets to disk
    """

    def __init__(self, data_ingestion_config: DataIngestionConfig):
        """
        Initialize the DataIngestion class with its configuration.

        Args:
            data_ingestion_config: Configuration object containing
            file paths and split parameters.
        """
        self.data_ingestion_config = data_ingestion_config

    def initiate_data_ingestion(self) -> tuple[str, str]:
        """
        Executes the data ingestion pipeline.

        Steps:
        1. Read raw CSV data
        2. Save raw data to artifacts location
        3. Split data into training and testing sets
        4. Save train and test datasets
        5. Return paths required for downstream transformation

        Returns:
            A DataTransformationConfig object containing
            paths to train and test datasets.
        """
        logger.info("Starting data ingestion process")

        try:
            # Read the raw dataset from the notebooks directory.
            # This is the initial data source before pipeline processing.
            df = pd.read_csv('notebooks/data/stud.csv')
            logger.info("Successfully read the raw data")

            # Ensure the directory structure for saving artifacts exists.
            # os.path.dirname extracts the parent directory from the file path.
            os.makedirs(
                os.path.dirname(self.data_ingestion_config.train_data_path),
                exist_ok=True
            )

            # Save a copy of the raw data for traceability and debugging.
            df.to_csv(self.data_ingestion_config.raw_data_path, index=False)
            logger.info("Raw data saved successfully")

            # Split the dataset into training and testing sets.
            # test_size controls the proportion of test data.
            # random_state ensures reproducibility.
            train_set, test_set = train_test_split(
                df,
                test_size=self.data_ingestion_config.test_size,
                random_state=42
            )

            # Persist the training dataset to disk.
            train_set.to_csv(
                self.data_ingestion_config.train_data_path,
                index=False
            )

            # Persist the testing dataset to disk.
            test_set.to_csv(
                self.data_ingestion_config.test_data_path,
                index=False
            )

            logger.info("Data ingestion completed successfully")

            # Return a configuration object required by the
            # data transformation stage of the pipeline.
            return DataTransformationConfig(
                train_data_path=self.data_ingestion_config.train_data_path,
                test_data_path=self.data_ingestion_config.test_data_path
            )

        except Exception as e:
            # Log the error at ERROR level for observability
            logger.error("Error occurred during data ingestion")

            # Wrap and raise the exception using CustomException
            # to preserve traceback and add contextual information
            raise CustomException(e, sys) from e
