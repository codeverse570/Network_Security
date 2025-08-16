from Network_security.components.data_ingestion import DataIngestion,DataIngestionConfig
from Network_security.entity.artifact_config import ArtificatConfig,DataValidationArtifact
from Network_security.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig,DataValidationConfig,DataTransformationConfig,ModelTrainerConfig
from Network_security.components.data_validation import DataValidation
from Network_security.components.data_transformation import DataTransformation
from Network_security.components.model_trainer import ModelTrainer
if __name__=='__main__':
      training_data_config= TrainingPipelineConfig()
      data_ingestion_config= DataIngestionConfig(training_data_config)
      dataIngestion= DataIngestion(data_ingestion_config)
      dataIngestionArtifact=dataIngestion.initiate_data_ingestion()
      
      dataValidation= DataValidation(dataIngestionArtifact=dataIngestionArtifact,dataValidationConfig=DataValidationConfig(training_data_config))
      dataValidationArtifact=dataValidation.intiateDataValidation()
      dataTransformationConfig=DataTransformationConfig(training_pipeline_config=training_data_config)
      dataTransformation= DataTransformation(dataValidationArtifact=dataValidationArtifact,dataTransformationConfig=dataTransformationConfig)
      dataTransformationArtifact=dataTransformation.initate_data_transformation()
      modelTrainer= ModelTrainer(dataTransformationArtifact,ModelTrainerConfig(training_data_config))
      print(modelTrainer.intiate_model_trainer())