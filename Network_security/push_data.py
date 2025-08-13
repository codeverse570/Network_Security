import sys
import pandas as pd
from Network_security.logging.logger import logging
import json
from Network_security.db import client
class NetworkDataExtract():
    def __init__(self):
        pass
    def convert_data_to_json(self, file_path):
        try:
            data_df= pd.read_csv(file_path)
            logging.info(f"Data extracted successfully from {file_path}")
            data_df.reset_index(drop=True, inplace=True)
           
            json_data_string = data_df.to_json(orient='records')
            json_data_raw= json.loads(json_data_string)
            return json_data_raw
        except Exception as e:
            logging.error(f"Error in converting data to JSON: {str(e)}")
            raise e 
    def push_to_mongo(self,records,database,collection):
        self.database= database
        self.records= records
        self.collection= collection
        self.database= client.get_database(self.database)
        self.collection= self.database[self.collection]
        self.collection.insert_many(records)
        return len(self.records)
        pass
if __name__ == "__main__":
    try:
        file_path = "Network_Data/phisingData.csv"  # Replace with your actual file path   
        network_data_extractor = NetworkDataExtract()
        json_data = network_data_extractor.convert_data_to_json(file_path)
        network_data_extractor.push_to_mongo(json_data,'network_security','NetworkData')  # Print or use the JSON data as needed
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        raise e