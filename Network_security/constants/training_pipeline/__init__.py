import os
import numpy

DATA_INGESTION_COLLECTION_NAME='NetworkData'
DATA_INGESTION_DATABASE_NAME='network_security'
DATA_INGESTION_DIR_NAME='data_ingestion'
DDATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR='ingested'
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO=0.2


TARGET_COLUMN='Result'
PIPELINE_NAME: str = "NetworkSecurity"
PIPELINE_DIR='NetworkSecurity'
ARTIFACT_DIR="Artificats"
FILENAME='NetworkData.csv'
TRAIN_FILE_NAME='train.csv'
TEST_FILE_NAME='test.csv'