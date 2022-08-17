



from email.mime import base
import sys, os
from insurance.constants import MODEL_TRAINER_BASE_ACCURACY_KEY
from insurance.exception import InsuranceException
from insurance.logger import logging
from insurance.config.configuration import Configuration
from insurance.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact
from insurance.entity.config_entity import ModelTrainerConfig
from typing import List
from insurance.entity.model_factory import ModelFactory, evaluate_regression_model, GridSearchedBestModel, MetricInfoArtifact
from insurance.utils.utils import load_object, save_object, load_numpy_array_data

class InsurancePremiumEstimator:
    def __init__(self, preprocessing_object, trained_model_object):
        """
        TrainedModel constructor
        preprocessing_object: preprocessing_object
        trained_model_object: trained_model_object
        """
        self.preprocessing_object = preprocessing_object
        self.trained_model_object = trained_model_object

    def predict(self, X):
        """
        function accepts raw inputs and then transformed raw input using preprocessing_object
        which gurantees that the inputs are in the same format as the training data
        At last it perform prediction on transformed features
        """
        transformed_feature = self.preprocessing_object.transform(X)
        return self.trained_model_object.predict(transformed_feature)

    def __repr__(self):
        return f"{type(self.trained_model_object).__name__}()"

    def __str__(self):
        return f"{type(self.trained_model_object).__name__}()"

class ModelTrainer:


    def __init__(self, model_trainer_config: ModelTrainerConfig, data_tansformation_artifact: DataTransformationArtifact):

        try:
            logging.info(f"{'>>>'*20} Model trainer log started {'<<<'*20}")
            self.model_trainer_config = model_trainer_config
            self.data_tranformation_artifact = data_tansformation_artifact

        except Exception as e:
            raise InsuranceException(e, sys) from e
    

    def initiate_model_trainer(self):

        try:

            ### getting the transformed train and test data from transformed_artifacts
            logging.info("getting the transformed train and test data from transformed_artifacts")
            transformed_train_arr_path = self.data_tranformation_artifact.transformed_train_path
            transformed_train_arr = load_numpy_array_data(file_path=transformed_train_arr_path)

            transformed_test_arr_path = self.data_tranformation_artifact.transformed_test_path
            transformed_test_arr = load_numpy_array_data(file_path=transformed_test_arr_path)

            ### dividing the input and target features for both train and test 
            logging.info("dividing the input and target features for both train and test ")
            train_x, train_y = transformed_train_arr[:,:-1], transformed_train_arr[:,-1]
            test_x, test_y = transformed_test_arr[:,:-1], transformed_test_arr[:,-1]
            
            ### extracting the model_config_file_path from model_trainer_config
            logging.info("extracting the model_config_file_path from model_trainer_config")
            model_config_path = self.model_trainer_config.model_config_file_path
            os.path.exists(model_config_path)

            logging.info(f"Initializing the model factory with the {model_config_path}")
            model_factory = ModelFactory(model_config_path= model_config_path)

            base_accuracy = self.model_trainer_config.base_accuracy
            logging.info(f" Expected_base_accuracy : {base_accuracy}")
            
            ### Initializing operation of best model selection on both training and testing dataset
            logging.info("Initializing operation of model selection")
            best_model = model_factory.get_best_model(input_features=train_x,
                                                     output_features= train_y,
                                                     base_accuracy=base_accuracy)
            logging.info(f"best model found on training dataset : {best_model}")

            logging.info(f"Extracting trained model list.")
            grid_searched_best_model_list:List[GridSearchedBestModel]=model_factory.grid_searched_best_model_list
            
            model_list = [model.best_model for model in grid_searched_best_model_list ]
            logging.info(f"Evaluation all trained model on training and testing dataset both")
            metric_info:MetricInfoArtifact = evaluate_regression_model(model_list=model_list,
                                                                        X_train=train_x,
                                                                        y_train=train_y,
                                                                        X_test=test_x,
                                                                        y_test=test_y,
                                                                        base_accuracy=base_accuracy)

            logging.info(f"Best found model on both training and testing dataset : {metric_info.model_object} with accuracy = {metric_info.model_accuracy}")
            
            ### Saving the preprocessing object and model object as combined Inusurance_premium_estimator model
            preprocessing_obj=  load_object(file_path=self.data_tranformation_artifact.preprocessed_pkl_path)
            model_object = metric_info.model_object


            trained_model_file_path=self.model_trainer_config.trained_model_file_path
            housing_model = InsurancePremiumEstimator(preprocessing_object=preprocessing_obj,trained_model_object=model_object)
            logging.info(f"Saving model at path: {trained_model_file_path}")
            save_object(file_path=trained_model_file_path,obj=housing_model)


            model_trainer_artifact=  ModelTrainerArtifact(is_trained=True,message="Model Trained successfully",
            trained_model_file_path=trained_model_file_path,
            train_rmse=metric_info.train_rmse,
            test_rmse=metric_info.test_rmse,
            train_accuracy=metric_info.train_accuracy,
            test_accuracy=metric_info.test_accuracy,
            model_accuracy=metric_info.model_accuracy
            
            )

            logging.info(f"Model Trainer Artifact: {model_trainer_artifact}")
            return model_trainer_artifact

            logging.info(f"Best found model on both training and testing dataset.")
        except Exception as e:
            raise InsuranceException(e,sys) from e
    def __del__(self):
        logging.info(f"{'>>'*30}Model Trainer log completed.{'<<'*30} \n\n")


#loading transformed training and testing datset
#reading model config file 
#getting best model on training datset
#evaludation models on both training & testing datset -->model object
#loading preprocessing pbject
#custom model object by combining both preprocessing obj and model obj
#saving custom model object
#return model_trainer_artifact