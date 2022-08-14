import yaml
from insurance.exception import InsuranceException
import sys


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