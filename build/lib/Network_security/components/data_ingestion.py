from Network_security.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig
from Network_security.entity.artifact_config import ArtificatConfig
from Network_security.exceptions import custom_exception
from Network_security.db import client
from Network_security.logging.logger import logging

import os
import sys
import pymongo
import pandas as pd 
from sklearn.model_selection import train_test_split
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
           self.collection_name = dataIngestionConfig.collection_name
           self.database_name = dataIngestionConfig.database_name

    def initiate_data_ingestion(self):
          try:
                logging.info("Reading Data from Database")
                database= client[self.database_name]
                collection= database[self.collection_name]
                json_data= collection.find()
                
                df=pd.json_normalize(json_data)
                df.drop("_id",axis=1,inplace=True)
                logging.info("Data Reading completed successfully!")
                logging.info("spliting in train and test data")
                train_data, test_data= train_test_split(df,test_size=self.train_test_split_ratio,random_state=42)
                os.makedirs(os.path.dirname(self.training_file_path),exist_ok=True)
                os.makedirs(os.path.dirname(self.testing_file_path),exist_ok=True)
                train_data.to_csv(self.training_file_path)

                test_data.to_csv(self.testing_file_path)
                return ArtificatConfig(self.training_file_path,self.testing_file_path)
                pass
          except Exception as e:
                raise custom_exception(e, sys)
          
if __name__=='__main__':
      training_data_config= TrainingPipelineConfig()
      data_ingestion_config= DataIngestionConfig(training_data_config)
      dataIngestion= DataIngestion(data_ingestion_config)
      dataIngestion.initiate_data_ingestion()