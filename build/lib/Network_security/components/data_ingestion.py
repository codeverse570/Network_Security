from Network_security.entity.config_entity import DataIngestionConfig
from Network_security.exceptions import custom_exception
from Network_security.db import client

import os
import sys
import pymongo
import pandas as pd 
import sklearn
from dotenv import load_dotenv
load_dotenv()
MONGO_DB_URL=os.getenv("MONGO_DB_URL")

class DataIngestion:
    def __init__(self,dataIngestionConfig:DataIngestionConfig):
           self.data_ingestion_dir= dataIngestionConfig.data_ingestion_dir
           self.feature_store_file_path= dataIngestionConfig.feature_store_file_path
           self.training_file_path= dataIngestionConfig.training_file_path
           self.testing_file_path = dataIngestionConfig.testing_file_path
           self.train_test_split_ratio = dataIngestionConfig.train_test_split_ratio
           self.collection_name = dataIngestionConfig.DATA_INGESTION_COLLECTION_NAME
           self.database_name = dataIngestionConfig.DATA_INGESTION_DATABASE_NAME

    def initiate_data_ingestion(self):
          try:
                pass
          except Exception as e:
                raise custom_exception(e, sys)