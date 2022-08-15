


from random import random
from insurance.entity.artifact_entity import DataIngestionArtifact
from insurance.entity.config_entity import DataIngestionConfig
from insurance.exception import InsuranceException
from insurance.logger import logging
import numpy as np
# from six.moves import urllib
import os, sys
import zipfile
import pandas as pd
from sklearn.model_selection import StratifiedShuffleSplit
import shutil


class DataIngestion:

    def __init__(self, data_ingestion_config: DataIngestionConfig):
        
        try:
            logging.info(f"{'>>'*20} logging for dataIngestion started {'<<'*20}")
            self.data_ingestion_config = data_ingestion_config

        except Exception as e:
            raise InsuranceException(e,sys) from e
    
    
    # def download_insurance_data(self):
        
    #     try:
    #         pass
        
    #     except Exception as e:
    #         logging.exception(InsuranceException(e,sys))
    #         raise InsuranceException(e,sys) from e

    def extract_zip_file(self, zip_file_path:str):
        """
        The extract_zip_file function extracts the zip file into a raw data directory.

        :param self: Allow the function to refer to and modify the containing class
        :param zip_file_path:str: Specify the path to the zip file that needs to be extracted
        
        :return: None

        :author: anil
        """
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir
            if os.path.exists(raw_data_dir):
                shutil.rmtree(path=raw_data_dir)
            os.makedirs(raw_data_dir, exist_ok=True)
            
            logging.info(f"Extracting zip file: [{zip_file_path}] into dir: [{raw_data_dir}]")
            with zipfile.ZipFile(zip_file_path,"r") as zip_ref:
                zip_ref.extractall(path=raw_data_dir)
            logging.info(f"Extraction completed")
        except Exception as e:
            raise InsuranceException(e,sys) from e

    def split_data_as_train_test(self):
        
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir

            file_name = os.listdir(raw_data_dir)[0]

            insurance_file_path = os.path.join(raw_data_dir,file_name)
            logging.info(f"Reading csv file: [ {insurance_file_path}]")
            insurance_data_frame = pd.read_csv(insurance_file_path)

            insurance_data_frame["expense_cat"] = pd.cut(insurance_data_frame["expenses"],
                                                [0.0,15000,30000,45000,60000,75000,np.inf],
                                                labels=[1,2,3,4,5,6])

            logging.info("splitting data into train and test")
            stratifed_test_set = None
            stratified_train_set = None

            split = StratifiedShuffleSplit(n_splits=1,test_size=0.25,random_state=42)
            
            for train_index,test_index in split.split(insurance_data_frame, insurance_data_frame["expense_cat"]):
                strat_train_set = insurance_data_frame.loc[train_index].drop(["expense_cat"],axis=1)
                strat_test_set = insurance_data_frame.loc[test_index].drop(["expense_cat"],axis=1)
        
            if strat_train_set is not None:
                train_file_path = os.path.join(self.data_ingestion_config.ingested_train_dir,file_name)
                logging.info(f"saving the train data to {train_file_path}")

                os.makedirs(self.data_ingestion_config.ingested_train_dir,exist_ok=True)

                strat_train_set.to_csv(train_file_path,index=False)

            if strat_test_set is not None:
                test_file_path = os.path.join(self.data_ingestion_config.ingested_test_dir,file_name)
                logging.info(f"saving the train data to {test_file_path}")

                os.makedirs(self.data_ingestion_config.ingested_test_dir,exist_ok=True)

                strat_test_set.to_csv(test_file_path,index=False)

            data_ingestion_artifact = DataIngestionArtifact(train_file_path = train_file_path, 
                                            test_file_path = test_file_path,
                                            is_generated = True,
                                            message= "Data ingestion completed succesfully")
            return data_ingestion_artifact

        except Exception as e:
            raise InsuranceException(e,sys) from e
        

    def initiate_data_ingestion(self)-> DataIngestionArtifact:
        
        try:
            zip_file_path = self.data_ingestion_config.zip_dataset_file_path
            self.extract_zip_file(zip_file_path=zip_file_path)
            return self.split_data_as_train_test()

        except Exception as e:
            raise InsuranceException(e,sys) from e

    def __del__(self):
        logging.info(f"{'>>'*20} Data ingestioin log completed {'<<'*20}")