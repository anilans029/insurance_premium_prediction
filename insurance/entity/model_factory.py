




from asyncore import read
from collections import namedtuple
from modulefinder import Module
from typing import List
import importlib
import sys
from insurance.exception import InsuranceException
from insurance.logger import logging
from insurance.utils.utils import read_yaml_file
from insurance.constants import GRID_SEARCH_KEY, SEARCH_PARAM_GRID_KEY, MODEL_SELECTION_KEY,MODULE_KEY,CLASS_KEY, PARAM_KEY
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

InitializedModelDetail = namedtuple("InitializedModelDetail", ["model_serial_number",
                                                                "model_obj",
                                                                "params_grid_search",
                                                                "model_name"])

GridSearchedBestModel = namedtuple("GridSearchedBestModel", ["model_serial_number",
                                                            "model",
                                                            "best_model",
                                                            "best_parameters",
                                                            "best_score"])

BestModel = namedtuple("BestModel", ["model_serial_number",
                                    "model",
                                    "best_model",
                                    "best_parameters",
                                    "best_score"])

MetricInfoArtifact = namedtuple("MetricInfoArtifact",
                                ["model_name", "model_object", "train_rmse", "test_rmse", "train_accuracy",
                                 "test_accuracy", "model_accuracy", "index_number"])

class ModelFactory:

    def __init__(self, model_config_path: str =None):
        try:
            self.model_config: dict = read_yaml_file(filepath=model_config_path)
            
            self.grid__search_csv_module = self.model_config[GRID_SEARCH_KEY][MODULE_KEY]
            self.grid_search_cv_class = self.model_config[GRID_SEARCH_KEY][CLASS_KEY]
            self.grid_search_cv_propertry_data= self.model_config[GRID_SEARCH_KEY][PARAM_KEY]
            self.all_models_intialization_config: dict = dict(self.model_config[MODEL_SELECTION_KEY])

            self.initialized_model_list = None
            self.grid_searched_best_model_list = None
        except Exception as e:
            raise InsuranceException(e,sys) from e


    @staticmethod
    def get_class_for_name(moduel_name:str, class_name:str):
        try:
            ### this will import the rquired module and raise import error if that module cant be imported
            module = importlib.import_module(moduel_name)
            logging.info(f"Executing command: from {module} import {class_name}")
            class_ref = getattr(module, class_name)
            return class_ref
        except Exception as e:
            raise InsuranceException(e,sys) from e
    @staticmethod
    def update_model_property_data(model_obj, property_data):
        try:
            if not isinstance(property_data, dict):
                raise Exception(f"property_data prarameter required to be dictionary")

            for key, value in property_data.items():
                logging.info(f"executing: {str(model_obj)}.{key}= {value}")
                setattr(model_obj,key, value)
            return model_obj

        except Exception as e:
            raise InsuranceException(e,sys) from e

    def get_initialized_model_list(self)->List[InitializedModelDetail]:
        try:
            initialized_model_list = []
            for model_serial_number in self.all_models_intialization_config.keys():
                single_model_initialization_config = self.all_models_intialization_config[model_serial_number]
                model_obj_reference = ModelFactory.get_class_for_name(moduel_name=single_model_initialization_config[MODULE_KEY],
                                                                class_name= single_model_initialization_config[CLASS_KEY])
                model_obj = model_obj_reference()
                
                ### obtaining the model_property_data params for this specific model_object
                if PARAM_KEY in single_model_initialization_config:
                    model_obj_property_data = dict(single_model_initialization_config[PARAM_KEY])
                    model_obj = ModelFactory.update_model_property_data(model_obj = model_obj,
                                                                        property_data = model_obj_property_data)
                
                ### obtaining the grid_search params for this specific model_object
                grid_params_search = single_model_initialization_config[SEARCH_PARAM_GRID_KEY]

                model_name = f"{single_model_initialization_config[MODULE_KEY]}.{single_model_initialization_config[CLASS_KEY]}"
                initialized_model_list.append(InitializedModelDetail(model_serial_number=model_serial_number,
                                                                    model_name= model_name,
                                                                    model_obj=model_obj,
                                                                    params_grid_search=grid_params_search))
            self.initialized_model_list = initialized_model_list
            return initialized_model_list

        except Exception as e:
            raise InsuranceException(e, sys) from e

    def execute_grid_search_operation(self, initialized_model: InitializedModelDetail, input_feature,
                                      output_feature) -> GridSearchedBestModel:
        """
        excute_grid_search_operation(): function will perform paramter search operation and
        it will return you the best optimistic  model with best paramter:
        estimator: Model object
        param_grid: dictionary of paramter to perform search operation
        input_feature: your all input features
        output_feature: Target/Dependent features
        ================================================================================
        return: Function will return GridSearchOperation object
        """
        try:
            # instantiating GridSearchCV class
            
           
            grid_search_cv_ref = ModelFactory.get_class_for_name(moduel_name=self.grid__search_csv_module,
                                                             class_name=self.grid_search_cv_class
                                                             )

            grid_search_cv = grid_search_cv_ref(estimator=initialized_model.model_obj,
                                                param_grid=initialized_model.params_grid_search)
            grid_search_cv = ModelFactory.update_model_property_data(grid_search_cv,
                                                                   self.grid_search_cv_propertry_data)

            
            message1 = f"{'**'* 15} Training {type(initialized_model.model_obj).__name__} Started. {'**'*15}"
            logging.info(message1)
            grid_search_cv.fit(input_feature, output_feature)
            message2 = f"{'**'* 15} Training {type(initialized_model.model_obj).__name__} completed {'**'* 15}"
            logging.info(message2)
            grid_searched_best_model = GridSearchedBestModel(model_serial_number=initialized_model.model_serial_number,
                                                             model=initialized_model.model_obj,
                                                             best_model=grid_search_cv.best_estimator_,
                                                             best_parameters=grid_search_cv.best_params_,
                                                             best_score=grid_search_cv.best_score_
                                                             )
            
            return grid_searched_best_model
        except Exception as e:
            raise InsuranceException(e, sys) from e


    def start_best_parameter_search_for_initialized_model(self, initialized_model: InitializedModelDetail,
                                                             input_feature,
                                                             output_feature) -> GridSearchedBestModel:
        """
        initiate_best_model_parameter_search(): function will perform paramter search operation and
        it will return you the best optimistic  model with best paramter:
        estimator: Model object
        param_grid: dictionary of paramter to perform search operation
        input_feature: your all input features
        output_feature: Target/Dependent features
        ================================================================================
        return: Function will return a GridSearchOperation
        """
        try:
            return self.execute_grid_search_operation(initialized_model=initialized_model,
                                                      input_feature=input_feature,
                                                      output_feature=output_feature)
        except Exception as e:
            raise InsuranceException(e, sys) from e

    def initiate_best_parameter_search_for_initialized_models(self,
                         initialized_model_list: List[InitializedModelDetail],
                         input_features,
                         output_features)-> List[GridSearchedBestModel]:
        try:
            self.grid_searched_best_model_list = []
            for initialized_model in initialized_model_list:
                grid_searched_best_model = self.start_best_parameter_search_for_initialized_model(initialized_model= initialized_model,
                                                                                                   input_feature= input_features ,
                                                                                                     output_feature=output_features)
                self.grid_searched_best_model_list.append(grid_searched_best_model)
            return self.grid_searched_best_model_list                                                                               
        
        except Exception as e:
            raise InsuranceException(e,sys) from e
    
    def get_best_model(self, input_features, output_features, base_accuracy = 0.6)-> BestModel:
        try:

            logging.info("started Initializing model from config file")
            initialized_model_list = self.get_initialized_model_list()

            logging.info(f"initialized_model_list = {initialized_model_list}")
            grid_searched_best_model_list = self.initiate_best_parameter_search_for_initialized_models(
                                                    initialized_model_list= initialized_model_list,
                                                    input_features = input_features,
                                                    output_features = output_features)
            logging.info(f"*********************The model_list is : [{grid_searched_best_model_list}*******************]")
            best_model = ModelFactory.get_best_model_from_grid_searched_best_model_list(grid_searched_best_model_list =grid_searched_best_model_list,
                                                                                        base_accuracy= base_accuracy)
            return best_model
                                                                            
        except Exception as e:
            raise InsuranceException(e,sys) from e

    def get_best_model_from_grid_searched_best_model_list(grid_searched_best_model_list,
                                                        base_accuracy)-> BestModel: 
        try:
            best_model = None
            for grid_searched_best_model in grid_searched_best_model_list:
                print(grid_searched_best_model)
                if base_accuracy < grid_searched_best_model.best_score:
                    logging.info(f"Acceptable model found:{grid_searched_best_model}")
                    
                    base_accuracy = grid_searched_best_model.best_score
                    best_model = grid_searched_best_model
            if not best_model:
                    raise Exception(f"None of Model has base accuracy >= {base_accuracy}")
            logging.info(f"Best Model: {best_model}")
            return best_model

        except Exception as e:
            raise InsuranceException(e, sys) from e

def evaluate_regression_model(model_list: list, X_train:np.ndarray, y_train:np.ndarray, X_test:np.ndarray, y_test:np.ndarray, base_accuracy:float=0.6) -> MetricInfoArtifact:
    """
    Description:
    This function compare multiple regression model return best model

    Params:
    model_list: List of model
    X_train: Training dataset input feature
    y_train: Training dataset target feature
    X_test: Testing dataset input feature
    y_test: Testing dataset input feature

    return
    It retured a named tuple
    
    MetricInfoArtifact = namedtuple("MetricInfo",
                                ["model_name", "model_object", "train_rmse", "test_rmse", "train_accuracy",
                                 "test_accuracy", "model_accuracy", "index_number"])

    """
    try:
        
    
        index_number = 0
        metric_info_artifact = None
        for model in model_list:
            model_name = str(model)  #getting model name based on model object
            logging.info(f"{'**'* 15}Started evaluating model: [{type(model).__name__}] {'**'* 15}")
            
            #Getting prediction for training and testing dataset
            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)

            #Calculating r squared score on training and testing dataset
            train_acc = r2_score(y_train, y_train_pred)
            test_acc = r2_score(y_test, y_test_pred)
            
            #Calculating mean squared error on training and testing dataset
            train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
            test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))

            # Calculating harmonic mean of train_accuracy and test_accuracy
            model_accuracy = (2 * (train_acc * test_acc)) / (train_acc + test_acc)
            diff_test_train_acc = abs(test_acc - train_acc)
            
            #logging all important metric
            logging.info(f"{'**'* 15} Score {'**'* 15}")
            logging.info(f"Train Score\t\t Test Score\t\t Average Score")
            logging.info(f"{train_acc}\t\t {test_acc}\t\t{model_accuracy}")

            logging.info(f"{'**'* 15} Loss {'**'* 15}")
            logging.info(f"Diff test train accuracy: [{diff_test_train_acc}].") 
            logging.info(f"Train root mean squared error: [{train_rmse}].")
            logging.info(f"Test root mean squared error: [{test_rmse}].")


            #if model accuracy is greater than base accuracy and train and test score is within certain thershold
            #we will accept that model as accepted model
            if model_accuracy >= base_accuracy and diff_test_train_acc < 0.05:
                base_accuracy = model_accuracy
                metric_info_artifact = MetricInfoArtifact(model_name=model_name,
                                                        model_object=model,
                                                        train_rmse=train_rmse,
                                                        test_rmse=test_rmse,
                                                        train_accuracy=train_acc,
                                                        test_accuracy=test_acc,
                                                        model_accuracy=model_accuracy,
                                                        index_number=index_number)

                logging.info(f"Acceptable model found {metric_info_artifact}. ")
            index_number += 1
        if metric_info_artifact is None:
            logging.info(f"No model found with higher accuracy than base accuracy")
            return MetricInfoArtifact(model_name=None,
                                                        model_object=None,
                                                        train_rmse=None,
                                                        test_rmse=None,
                                                        train_accuracy=None,
                                                        test_accuracy=None,
                                                        model_accuracy=None,
                                                        index_number=None)
        return metric_info_artifact
    except Exception as e:
        raise InsuranceException(e, sys) from e

