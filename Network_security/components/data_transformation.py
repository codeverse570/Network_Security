import numpy as np 
import pandas as pd
from Network_security.exceptions import custom_exception
from Network_security.logging.logger import logging
from Network_security.entity.artifact_config import DataValidationArtifact,DataTransformationArtifact
from Network_security.entity.config_entity import DataTransformationConfig
from Network_security.constants.training_pipeline import TARGET_COLUMN,DATA_TRANSFORMATION_IMPUTER_PARAMS
from sklearn.compose import ColumnTransformer
from Network_security.utils.main_utils.utils import save_array_file,save_object
from sklearn.preprocessing import StandardScaler
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
import sys
class DataTransformation:
    def __init__(self,dataValidationArtifact:DataValidationArtifact,dataTransformationConfig:DataTransformationConfig):
        try:
            self.dataValidationArtifact= dataValidationArtifact
            self.dataTransformationConfig=dataTransformationConfig
        except Exception as e:
            raise custom_exception(e,sys)
    def transformation_pipeline(self):
        try:
            transformer= Pipeline([('imputer',KNNImputer(** DATA_TRANSFORMATION_IMPUTER_PARAMS))])
            return transformer
            pass
        except Exception as e:
            raise custom_exception(e,sys)
    def initate_data_transformation(self):
         try:
             logging.info("Data Transformation Started!")
             train_df= pd.read_csv(self.dataValidationArtifact.valid_train_file_path)
             test_df= pd.read_csv(self.dataValidationArtifact.valid_test_file_path)
             y_train= train_df[TARGET_COLUMN].replace(-1,0)
             y_test= test_df[TARGET_COLUMN].replace(-1,0)
             x_train= train_df.drop(TARGET_COLUMN,axis=1)
             x_test= test_df.drop(TARGET_COLUMN,axis=1)
             transformer=self.transformation_pipeline()
             transformed_x_train= transformer.fit_transform(x_train)
             transformed_x_test= transformer.transform(x_test)
             train_array= np.c_[transformed_x_train,np.array(y_train)]
             test_array=np.c_[transformed_x_test,np.array(y_test)]
             save_array_file(self.dataTransformationConfig.transformed_train_file_path,train_array)
             save_array_file(self.dataTransformationConfig.transformed_test_file_path,test_array)
             save_object(self.dataTransformationConfig.transformed_object_file_path,transformer)
             return DataTransformationArtifact(transformed_object_file_path=self.dataTransformationConfig.transformed_object_file_path,transformed_test_file_path=self.dataTransformationConfig.transformed_test_file_path,transformed_train_file_path=self.dataTransformationConfig.transformed_train_file_path)
         except Exception as e:
             raise custom_exception(e,sys)
