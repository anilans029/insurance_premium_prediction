


import sys
from insurance.entity.artifact_entity import DataIngestionArtifact
from insurance.entity.config_entity import DataIngestionConfig
from insurance.config.configuration import Configuration
from insurance.exception import InsuranceException
from insurance.component.stage1_data_ingestion import DataIngestion
class Pipeline:

    def __init__(self,config : Configuration = Configuration())-> None:
        try:
            self.config = config
            print(self.config)
        except Exception as e:
            raise InsuranceException(e,sys)

    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            data_ingestion = DataIngestion(data_ingestion_config=self.config.get_data_ingestion_config())
            
            return data_ingestion.initiate_data_ingestion()

        except Exception as e:
            raise InsuranceException(e, sys) from e
    

    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            
        except Exception as e:
            raise InsuranceException(e, sys) from e