from Network_security.components.data_ingestion import DataIngestion,DataIngestionConfig
from Network_security.entity.artifact_config import ArtificatConfig,DataValidationArtifact
from Network_security.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig,DataValidationConfig,DataTransformationConfig,ModelTrainerConfig
from Network_security.components.data_validation import DataValidation
from Network_security.components.data_transformation import DataTransformation
from Network_security.components.model_trainer import ModelTrainer
from Network_security.exceptions import custom_exception
import sys

class TrainingPipeline:
     def __init__(self):
          self.training_config=TrainingPipelineConfig()
          pass
     def start_data_ingestion(self):
        try:
          data_ingestion_config= DataIngestionConfig(training_pipeline_config=self.training_config)
          self.data_ingestion_artifact= DataIngestion(data_ingestion_config).initiate_data_ingestion()
          return self.data_ingestion_artifact
        except Exception as e:
            raise custom_exception(e,sys)
     def start_data_validation(self):
          try:
              data_validation_config= DataValidationConfig(training_pipeline_config=self.training_config)
              self.data_validation_artifact= DataValidation(dataIngestionArtifact=self.data_ingestion_artifact,dataValidationConfig=data_validation_config).intiateDataValidation()
              return self.data_validation_artifact
          except Exception as e:
               raise custom_exception(e,sys)
     def start_data_transformation(self):
          try:
              data_transformation_config= DataTransformationConfig(training_pipeline_config=self.training_config)
              self.data_transformation_artifact= DataTransformation(dataTransformationConfig=data_transformation_config,dataValidationArtifact=self.data_validation_artifact).initate_data_transformation()
              return self.data_validation_artifact           
              pass
          except Exception as e:
              raise custom_exception(e,sys)
     def start_data_trainer(self):
          try:
              data_trainer_config= ModelTrainerConfig(training_pipeline_config=self.training_config)
              self.model_trainer_artifact= ModelTrainer(modelTrainerConfig=data_trainer_config,dataTransformationArtifact=self.data_transformation_artifact).intiate_model_trainer()
              return self.model_trainer_artifact           
              pass
          except Exception as e:
              raise custom_exception(e,sys)       
          
     def start_training_pipeline(self):
         try:
             self.start_data_ingestion()
             self.start_data_validation()
             self.start_data_transformation()
             return self.start_data_trainer() 
             pass
         except Exception as e:
             raise custom_exception(e,sys)