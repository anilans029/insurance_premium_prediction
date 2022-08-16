from collections import namedtuple

# ["dataset_download_url", "tgz_download_dir","raw_data_dir","ingested_train_dir","ingested_test_dir"]

DataIngestionConfig = namedtuple("DataIngestionConfig",
                                                     ["zip_dataset_file_path",
                                                     "raw_data_dir",
                                                    "ingested_train_dir",
                                                    "ingested_test_dir"])

DataVaidationConfig = namedtuple("DataVaidationConfig",
                                                      ["schema_file_path","report_file_path","report_page_file_path"])

# add_bedroom_per_romm : optional column to be added in dataset or not -> T or F
DataTransformation = namedtuple("DataTransformation",[
                                                    "add_bedroom_per_romm",
                                                    "transformed_train_dir",
                                                    "transformed_test_dir",
                                                    "preprocessed_object_file_path"])

ModelTrainerConfig = namedtuple("ModelTrainerConfig",
                                                    ["trained_model_file_path",
                                                    "base_accuracy"])

#  Model_Evaluation_file_path : it will containg path info of all the exising model in production
ModelEvaluationConfig = namedtuple("ModelEvaluationConfig",
                                                    ["Model_Evaluation_file_path",
                                                    "time_stamp"])

ModelPusherConfig = namedtuple("ModelPusherConfig",["export_dir_path"])

TrainPipelineConfig = namedtuple("TrainPipelineConfig", ["artifact_dir"])