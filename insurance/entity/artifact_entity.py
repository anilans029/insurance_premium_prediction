from collections import namedtuple

from .config_entity import DataTransformation


DataIngestionArtifact = namedtuple("DataIngestionArtifact",
                                ["train_file_path","test_file_path","is_generated","message"])

DataValidationArtifact = namedtuple("DataValidationArtifact",
["schema_file_path","report_file_path","report_page_file_path","is_validated","message"])

DataTransformationArtifact = namedtuple("DataTransformationArtifact",["is_Transformed","transformed_train_path","transformed_test_path","preprocessed_pkl_path","message"])