
import sys, os
from insurance.constants import *
from insurance.exception import InsuranceException
from insurance.logger import logging
from insurance.entity.artifact_entity import DataIngestionArtifact, DataTransformationArtifact, DataValidationArtifact
from insurance.entity.config_entity import DataTransformationConfig
import pandas as pd
import numpy as np
from insurance.utils.utils import read_yaml_file, load_data, save_numpy_array_data, save_object
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from sklearn.impute import SimpleImputer



class Data_Tranformation:


    def __init__(self, data_ingestion_artifact:DataIngestionArtifact,
                       data_validation_artifact: DataValidationArtifact,
                       data_transformation_config: DataTransformationConfig ):
        try:
            logging.info(f"{'>>'*30}Data Transformation log started.{'<<'*30} \n\n")
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config


        except Exception as e:
            raise InsuranceException(e,sys) from e

    def get_transformer_object(self):
        """
        The get_transformer_object function takes in the schema file path and returns a transformer object which can be used to transform the data.
        The transformer object is created by using ColumnTransformer from sklearn library. The ColumnTransformer takes in two arguments:
            1) Preprocessing objects for each column (numerical and categorical columns are processed separately)
            2) List of columns on which we need to apply these transformations 
        
        :param self: Access the attributes and methods of the class in python

        :return: A columntransformer object which is used to transform the features
        :author: anil
        """
        try:
            
            schema_file_path = self.data_validation_artifact.schema_file_path
            schema = read_yaml_file(schema_file_path)
            numerical_columns = schema[SCHEMA_NUMERICAL_COLUMNS_KEY]
            categorical_columns = schema[SCHEMA_CATEGORICAL_COLUMNS_KEY]

            logging.info(f"Categorical columns: {categorical_columns}")
            logging.info(f"Numerical columns: {numerical_columns}")

            numerical_col_preprocessing = Pipeline(steps=[("missing_values_proceesing", SimpleImputer(strategy="median")),
                                                          ("scaling values", StandardScaler())])

            categorical_col_preprocessing = Pipeline(steps=[("handling_categorical_col", OneHotEncoder(sparse=False,handle_unknown='ignore',drop='first')),
                                                            ("scaling_categorical_col_values",StandardScaler())])

            logging.info("Pre_processing the numerical and categorical features")
            preProcessing = ColumnTransformer([
                                                ("numerical_col_preprocessing",numerical_col_preprocessing,numerical_columns),
                                                ("categorical_col_preprocessing",categorical_col_preprocessing,categorical_columns)
                                                ])

            return preProcessing

        except Exception as e:
            raise InsuranceException(e,sys) from e


    def initiate_transformation(self):
        """
        The initiate_transformation function takes the data_ingestion_artifact, 
        data_validation_artifact and data transformation config as input. 
        It reads the train and test files from their paths, loads them into pandas dataframes. 
        Then it splits the input features from target feature in both train and test datasets.  
        After that it applies preprocessing on both training and testing dataset using a transformer object which is returned by get transformer object function.  
        Finally it saves transformed training file at transformed train path ,transformed testing file at transformed test path, preprocessed pkl file at preprocessed pkl path
        
        :param self: Access variables that belongs to the class

        :return: The datatransformationartifact object

        :author: anil
        """
        
        try:
            
            ### retrieving the filepaths of train, test files and schema files
            logging.info("getting the paths for the train, test, schema files")
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path
            schema_file_path = self.data_validation_artifact.schema_file_path
            logging.info(f"""obtained the paths for train_file: {[train_file_path],}
                                    test_file: {[test_file_path]},
                                    schema_file: {[schema_file_path]} """)

            ### reading the train and test files as dataframes and schema file 
            train_dataframe = load_data(train_file_path, schema_file_path)
            test_dataframe = load_data(test_file_path, schema_file_path)

            schema = read_yaml_file(schema_file_path)
            
            ### getting the input and targets column names from schema file
            
            target_column = schema[SCHEMA_TARGET_COLUMN_KEY]
            all_columns = schema[DATASET_SCHEMA_COLUMNS_KEY]

            ### splitting the input and target features for train and test dataframe
            input_feature_train_dataframe = train_dataframe.drop(columns=[target_column])
            target_train_dataframe = train_dataframe[target_column]

            input_feature_test_dataframe = test_dataframe.drop(columns=[target_column])
            target_test_dataframe = test_dataframe[target_column]


            ### getting the preprocessing column_transformer object
            pre_processing = self.get_transformer_object()

            ### applying the preprocessing on the input_features of train and test dataframes
            logging.info(f"Applying preprocessing on training and testing input features dataframe")
            transormed_input_train_arr = pre_processing.fit_transform(input_feature_train_dataframe)
            transormed_input_test_arr = pre_processing.transform(input_feature_test_dataframe)

            ### concatenating the transormed inp_features of train and test data with their respective target features
            train_arr = np.c_[transormed_input_train_arr, np.array(target_train_dataframe)]
            test_arr = np.c_[transormed_input_test_arr, np.array(target_test_dataframe)] 

            ### obtaining the tranformed train and test file name and paths for saving them
            transformed_train_dir = self.data_transformation_config.transformed_train_dir
            transformed_test_dir =  self.data_transformation_config.transformed_test_dir

            train_file_name = os.path.basename(train_file_path).replace(".csv",".npz")
            test_file_name = os.path.basename(test_file_path).replace(".csv",".npz")

            transformed_train_file_path = os.path.join(transformed_train_dir, train_file_name)
            transformed_test_file_path = os.path.join(transformed_test_dir, test_file_name)

            ### saving the test and train data arrays in their respective paths
            logging.info(f"Saving the preprocessed train file at {[transformed_train_file_path]} and test data files at {[transformed_test_file_path]}.")
            save_numpy_array_data(transformed_train_file_path,train_arr)
            save_numpy_array_data(transformed_test_file_path, test_arr)

            ### saving the preprocessed obj 
            logging.info(f"Saving preprocessing object.")
            preprocesed_obj_file_path = self.data_transformation_config.preprocessed_object_file_path
            save_object(file_path=preprocesed_obj_file_path, obj=pre_processing)

            data_transformation_artifact = DataTransformationArtifact(is_Transformed = True ,
                                       transformed_train_path = transformed_train_file_path ,
                                       transformed_test_path= transformed_test_file_path,
                                       preprocessed_pkl_path= preprocesed_obj_file_path,
                                       message= "Data Transformation completed succesfully")
            logging.info(data_transformation_artifact)
            return data_transformation_artifact


        except Exception as e:
            raise InsuranceException(e,sys) from e
    def __del__(self):
        logging.info(f"{'>>'*30}Data Transformation log completed.{'<<'*30} \n\n")