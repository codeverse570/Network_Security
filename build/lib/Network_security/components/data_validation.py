from Network_security.entity.artifact_config import DataValidationArtifact,ArtificatConfig
from Network_security.entity.config_entity import DataValidationConfig
from Network_security.constants.training_pipeline import SCHEMA_FILE_PATH
from Network_security.exceptions import custom_exception
from Network_security.utils.main_utils.utils import load_yaml_file,write_yaml_file
from Network_security.logging.logger import logging
from scipy.stats import ks_2samp
import pandas as pd
import sys
import os
class DataValidation:
    def __init__(self,dataValidationConfig:DataValidationConfig,dataIngestionArtifact:ArtificatConfig):
      
        self.dataValidationConfig= dataValidationConfig
        self.dataIngestionArtifact=dataIngestionArtifact
        self._scheme_config= load_yaml_file(SCHEMA_FILE_PATH)
        pass
    def readFile(self,file_path):
       try:
          file=pd.read_csv(file_path)
          return file
       except Exception as e:
          raise custom_exception(e,sys)
    def validateColumns(self,df:pd.DataFrame):
        try:
         logging.info(f"Number of columns in dataframe {len(df.columns)}")
         logging.info(f"Number of columns in schema {len(self._scheme_config)}")
         
         if len(self._scheme_config)==len(df.columns):
            return True
         else:
            return False
        except Exception as e:
           raise custom_exception(e,sys)
    def checkDataDrift(self,base_df,current_df,threshold=0.05):
          try:
             report={}
             isFound=False
             status=True
             for column in base_df.columns:
                base_col= base_df[column]
                current_col= current_df[column]
                drift= ks_2samp(base_col,current_col)
                if drift.pvalue <threshold:
                   status=False
                   isFound=True
                   report.update({
                      'p_value':float(drift.pvalue),
                      'drift_status':isFound
                   })
                else:
                   is_found=False
             drift_report_file= self.dataValidationConfig.drift_report_file_path
             
             os.makedirs(os.path.dirname(self.dataValidationConfig.drift_report_file_path),exist_ok=True)
             write_yaml_file(drift_report_file,report)
             return status
          except Exception as e:
             raise custom_exception(e,sys)
    def validateNumericalColumns(self,df:pd.DataFrame)-> bool:
        try:
            numerical_df = df.select_dtypes(include='number')
            num_numerical_cols = len(numerical_df.columns)

            logging.info(f"The number of numerical columns is: {num_numerical_cols}")
            if num_numerical_cols>0:
               return True
            else :return False
        except Exception as e:
           raise custom_exception(e,sys)        
    def intiateDataValidation(self):
       try:
         logging.info("data validation started..")
         train_df= self.readFile(self.dataIngestionArtifact.train_file)
         test_df= self.readFile(self.dataIngestionArtifact.test_file)
         status= self.validateColumns(train_df)
         if( status==False): error_message="train Columns not matched!"

         status= self.validateColumns(test_df)
         if(status==False): error_message ='test columns not matched!'
         status= self.checkDataDrift(train_df,test_df)
         if(not status): error_message='High Drift in Datasets'
         os.makedirs(os.path.dirname(self.dataValidationConfig.valid_train_file_path),exist_ok=True)
         train_df.to_csv(self.dataValidationConfig.valid_train_file_path,index=False,header=True)
         test_df.to_csv(self.dataValidationConfig.valid_test_file_path,index=False,header=True)
        #  return DataValidationArtifact()
         return DataValidationArtifact(validation_status=status,valid_test_file_path=self.dataValidationConfig.valid_test_file_path,invalid_test_file_path=None,invalid_train_file_path=None,drift_report_file_path=self.dataValidationConfig.drift_report_file_path,valid_train_file_path=self.dataValidationConfig.valid_train_file_path)
       except Exception as e:
          raise custom_exception(e,sys)