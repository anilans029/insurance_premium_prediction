


import sys
from insurance.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact, DataTransformationArtifact, ModelTrainerArtifact
from insurance.entity.config_entity import DataIngestionConfig
from insurance.config.configuration import Configuration
from insurance.exception import InsuranceException
from insurance.component.stage1_data_ingestion import DataIngestion
from insurance.component.stage2_data_validation import DataValidation
from insurance.component.stage3_data_transformation import Data_Tranformation
from insurance.component.stage4_model_trainer import ModelTrainer

class Pipeline:

    def __init__(self,config : Configuration = Configuration())-> None:
        try:
            self.config = config
        except Exception as e:
            raise InsuranceException(e,sys)

    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            data_ingestion = DataIngestion(data_ingestion_config=self.config.get_data_ingestion_config())
            
            return data_ingestion.initiate_data_ingestion()

        except Exception as e:
            raise InsuranceException(e, sys) from e
    
    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact)-> DataValidationArtifact:
        try:
            data_validation = DataValidation(dataValidation_config=self.config.get_data_validation_config(),
                                             data_ingestion_artifact=data_ingestion_artifact
                                             )
            return data_validation.initiate_data_validation()
        except Exception as e:
            raise InsuranceException(e, sys) from e

    def start_data_transformation(self,
                                  data_ingestion_artifact: DataIngestionArtifact,
                                  data_validation_artifact: DataValidationArtifact
                                  ) -> DataTransformationArtifact:
        try:
            data_transformation = Data_Tranformation(
                data_transformation_config=self.config.get_data_transformation_config(),
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_artifact=data_validation_artifact
            )
            return data_transformation.initiate_transformation()

        except Exception as e:
            raise InsuranceException(e, sys) from e

    def start_model_trainer(self, data_transformation_artifact: DataTransformationArtifact) -> ModelTrainerArtifact:
        try:
            model_trainer = ModelTrainer(model_trainer_config=self.config.get_model_trainer_cofig(),
                                         data_tansformation_artifact=data_transformation_artifact
                                         )
            model_trainer_artifact = model_trainer.initiate_model_trainer()

            return model_trainer_artifact
        except Exception as e:
            raise InsuranceException(e, sys) from e

    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validaion_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(
                                                                data_ingestion_artifact=data_ingestion_artifact,
                                                                data_validation_artifact=data_validaion_artifact
                                                                )
            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact=data_transformation_artifact)

        except Exception as e:
            raise InsuranceException(e, sys) from e