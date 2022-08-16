import shutil
import sys
from xml.dom import InuseAttributeErr
from insurance.entity.config_entity import *
from insurance.utils.utils import read_yaml_file
from insurance.constants import *
from insurance.logger import logging
from insurance.exception import InsuranceException
import os,sys



class Configuration:

    def __init__(self,config_file_path :str= CONFIG_FILE_PATH,current_time_stamp: str = CURRENT_TIME_STAMP) -> None:

        try:
            self.config_info = read_yaml_file(filepath=config_file_path)
            self.training_pipeline_config = self.get_training_pipeline_config()
            self.time_stamp = current_time_stamp
        except Exception as e:
            raise InsuranceException(e,sys) from e

    def get_data_ingestion_config(self)-> DataIngestionConfig:
        """
        The get_data_inagestion_config function returns a DataIngestionConfig object that contains the following:
            raw_data_dir: The directory where the raw data is located.
            ingested_train_dir: The directory where the ingested training data will be written to.
            ingested_test_dir: The directory where the ingested test data will be written to.
        
        :param self: Access the class instance inside of a method
        :return: A dataingestionconfig object

        :author: anil
        """
        try:
            artifact_dir = self.training_pipeline_config.artifact_dir
            data_ingestion_artifact_dir=os.path.join(artifact_dir,DATA_INGESTION_ARTIFACT_DIR )
            data_ingestion_info = self.config_info[DATA_INGESTION_CONFIG_KEY]

            zip_dataset_dir = data_ingestion_info[DATA_INGESTION_ZIP_DATASET_DIR_KEY]
            zip_file_name = data_ingestion_info[DATA_INGESTION_DATASET_ZIP_NAME_KEY]
            zip_file_path = os.path.join(data_ingestion_artifact_dir,zip_dataset_dir,zip_file_name)

            raw_data_dir = os.path.join(data_ingestion_artifact_dir,
            data_ingestion_info[DATA_INGESTION_RAW_DATA_DIR_KEY]
            )

            ingested_data_dir = os.path.join(
                data_ingestion_artifact_dir,
                data_ingestion_info[DATA_INGESTION_INGESTED_DIR_NAME_KEY]
            )
            ingested_train_dir = os.path.join(
                ingested_data_dir,
                data_ingestion_info[DATA_INGESTION_TRAIN_DIR_KEY]
            )
            ingested_test_dir =os.path.join(
                ingested_data_dir,
                data_ingestion_info[DATA_INGESTION_TEST_DIR_KEY]
            )


            data_ingestion_config=DataIngestionConfig(
                zip_dataset_file_path=zip_file_path,
                raw_data_dir=raw_data_dir, 
                ingested_train_dir=ingested_train_dir, 
                ingested_test_dir=ingested_test_dir
            )
            logging.info(f"Data Ingestion config: {data_ingestion_config}")
            return data_ingestion_config

        except Exception as e:
            raise InsuranceException(e,sys) from e

    def get_data_validation_config(self)-> DataVaidationConfig:
        try:
            artifact_dir = self.training_pipeline_config.artifact_dir
            data_validation_artifact_dir=os.path.join(artifact_dir,DATA_VALIDATION_ARTIFACT_DIR_NAME)
            data_validation_conif_info = self.config_info[DATA_VALIDATION_CONFIG_KEY]


            schema_file_path = os.path.join(ROOT_DIR,
                        data_validation_conif_info[DATA_VALIDATION_SCHEMA_DIR_KEY],
                        data_validation_conif_info[DATA_VALIDATION_SCHEMA_FILE_NAME_KEY])

            report_file_path = os.path.join(data_validation_artifact_dir,
                                            data_validation_conif_info[DATA_VALIDATION_REPORT_FILE_NAME_KEY])

            report_page_file_path = os.path.join(data_validation_artifact_dir,
                                            data_validation_conif_info[DATA_VALIDATION_REPORT_PAGE_FILE_NAME_KEY])

            dataValidationConfig = DataVaidationConfig(schema_file_path = schema_file_path,
                                                report_file_path= report_file_path,
                                                report_page_file_path=report_page_file_path)
            return dataValidationConfig
        except Exception as e:
            raise InsuranceException(e,sys) from e

    def get_data_transformation_config(self)-> DataTransformation:
        
        try:
            data_tranformation_config_info = self.config_info[DATA_TRANSFORMATION_CONFIG_KEY]
            data_transformation_dir =os.path.join(self.training_pipeline_config.artifact_dir,
                                                 DATA_TRANSFORMATION_ARTIFACT_NAME,
                                                 self.time_stamp)
                
            transformed_train_dir =os.path.join(data_transformation_dir,
                                                data_tranformation_config_info[DATA_TRANSFORMATION_TRANSFORMED_DIR_KEY],
                                                data_tranformation_config_info[DATA_TRANSFORMATION_TRANSFORMED_TRAIN_DIR_KEY])
            transformed_test_dir= os.path.join(data_transformation_dir,
                                                data_tranformation_config_info[DATA_TRANSFORMATION_TRANSFORMED_DIR_KEY],
                                                data_tranformation_config_info[DATA_TRANSFORMATION_TRANSFORMED_TEST_DIR_KEY])
            
            preprocessed_obj_file_path = os.path.join(data_transformation_dir,
                                                        data_tranformation_config_info[DATA_TRANSFORMATION_PREPROCESSING_DIR_KEY],
                                                        data_tranformation_config_info[DATA_TRANSFORMATION_PREPROCESSED_OBJECT_FILE_NAME_KEY])


            add_bedroom_per_romm = data_tranformation_config_info[DATA_TRANSFORMATION_ADD_BEDROOM_PER_ROOM_KEY]

            data_tranformation = DataTransformation( add_bedroom_per_romm= add_bedroom_per_romm ,
                                                transformed_train_dir = transformed_train_dir,
                                                transformed_test_dir = transformed_test_dir, 
                                                preprocessed_object_file_path= preprocessed_obj_file_path)
            return data_tranformation

        except Exception as e:
            raise InsuranceException(e,sys) from e

    def get_model_trainer_cofig(self)-> ModelTrainerConfig:
        pass

    def get_model_evaluation_cofig(self)-> ModelEvaluationConfig:
        pass

    def get_model_pusher_cofig(self)-> ModelPusherConfig:
        pass

    def get_training_pipeline_config(self)-> TrainPipelineConfig:
        """
        The get_training_pipeline_config function returns a TrainPipelineConfig object that contains the 
        artifact directory where the training artifacts will be stored. The artifact directory is specified in 
        the config file under TRAINING_PIPELINE_CONFIG_KEY, and it is located at {ROOT}/{TRAINING_PIPELINE}/{ARTIFACT}.
        
        :param self: Access variables that belongs to the class
        
        :return: A trainpipelineconfig object
        :author: anil
        """
        
        try:
            training_pipeline_config = self.config_info[TRAINING_PIPELINE_CONFIG_KEY]
            artifact_dir = os.path.join(ROOT_DIR,
                                        training_pipeline_config[TRAINING_PIPELINE_NAME_KEY],
                                        training_pipeline_config[TRAINING_PIPELINE_ARTIFACT_DIR_KEY]
                                        )

            training_pipeline_config = TrainPipelineConfig(artifact_dir=artifact_dir)
            logging.info(f"Training pipleine config: {training_pipeline_config}")
            return training_pipeline_config
        except Exception as e:
            raise InsuranceException(e,sys) from e
