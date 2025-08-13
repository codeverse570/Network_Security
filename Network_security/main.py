from Network_security.components.data_ingestion import DataIngestion,DataIngestionConfig
from Network_security.entity.artifact_config import ArtificatConfig
from Network_security.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig


if __name__=='__main__':
      training_data_config= TrainingPipelineConfig()
      data_ingestion_config= DataIngestionConfig(training_data_config)
      dataIngestion= DataIngestion(data_ingestion_config)
      dataIngestion.initiate_data_ingestion()