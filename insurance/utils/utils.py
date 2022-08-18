import yaml
from insurance.exception import InsuranceException
import sys
from insurance.constants import *
import pandas as pd
import numpy as np
import dill


def write_yaml_file(file_path:str,data:dict=None):
    """
    Create yaml file 
    file_path: str
    data: dict
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path,"w") as yaml_file:
            if data is not None:
                yaml.dump(data,yaml_file)
    except Exception as e:
        raise InsuranceException(e,sys)

def read_yaml_file(filepath: str)-> dict:
    """
    The read_yaml_file function reads a yaml file and returns the contents as a dictionary.
    
    :param filepath:str: Specify the location of the yaml file that is to be read
    :return: A dictionary that contains the contents of the yaml file
  
    :author: anil
    """
    
    try:
        with open(filepath,"rb") as yamlFile:
            return yaml.safe_load(yamlFile)
    except Exception as e:
        raise InsuranceException(e,sys) from e


def load_data(file_path: str, schema_file_path: str) -> pd.DataFrame:
    """
    The load_data function reads a CSV file and returns a Pandas DataFrame.
    The load_data function reads the schema from the YAML file to ensure that 
    the data types in the DataFrame match those defined by the schema. The 
    load_data function raises an exception if any column is not included in 
    the schema or has an incorrect type.
    
    :param file_path:str: Specify the path of the file that contains the data
    :param schema_file_path:str: Specify the path to the schema file

    :return: A pandas dataframe

    :author: anil
    """
    try:
        datatset_schema = read_yaml_file(schema_file_path)
        schema = datatset_schema[DATASET_SCHEMA_COLUMNS_KEY]
        dataframe = pd.read_csv(file_path)
        error_messgae = ""

        for column in dataframe.columns:
            if column in list(schema.keys()):
                dataframe[column].astype(schema[column])
            else:
                error_messgae = f"{error_messgae} \nColumn: [{column}] is not in the schema."
        if len(error_messgae) > 0:
            raise Exception(error_messgae)
        return dataframe

    except Exception as e:
        raise InsuranceException(e,sys) from e

def save_numpy_array_data(file_path: str, array: np.array):
    """
    Save numpy array data to file
    file_path: str location of file to save
    array: np.array data to save
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise InsuranceException(e, sys) from e


def load_numpy_array_data(file_path: str) -> np.array:
    """
    load numpy array data from file
    file_path: str location of file to load
    return: np.array data loaded
    """
    try:
        with open(file_path, 'rb') as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise InsuranceException(e, sys) from e


def save_object(file_path:str,obj):
    """
    file_path: str
    obj: Any sort of object
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)

    except Exception as e:
        raise InsuranceException(e,sys) from e


def load_object(file_path:str):
    """
    file_path: str
    """
    try:
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)

    except Exception as e:
        raise InsuranceException(e,sys) from e