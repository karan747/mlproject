import sys
from dataclasses import dataclass
import os

import numpy as np 
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifcats', "preprocessor.pkl")

class DataTransformation:
    def __init__(self) -> None:
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_obj(self):
        
        try:
            numeric_columns=["writing_score", "reading_score"]
            categorical_columns = ['gender','race_ethnicity','parental_level_of_education','lunch','test_preparation_course',]
            num_pipeline =  Pipeline(
                steps=[
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler(with_mean=False))
                ]
            )

            logging.info("numerical columns scaling done")

            cat_pipeline = Pipeline(
                steps = [
                ("imputer", SimpleImputer(strategy='most_frequent')),
                ("one_hot_encoder", OneHotEncoder()),
                ("scaler", StandardScaler(with_mean=False))
                ]
            )

            logging.info("Categorical columns encoding done")

            preprocessor = ColumnTransformer(
                [
                ("num_pipeline", num_pipeline , numeric_columns),
                ("cat_pipelines", cat_pipeline, categorical_columns)
                ]
            )
             
            return preprocessor


        except Exception as e:
            raise CustomException(e, sys)
    
    def initiate_data_transformation (self, train_path, test_path):
        try:
            logging.info("Data transformation initiated")
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("data reading done")
            logging.info("preprocessing starts")

            preprocessing_obj = self.get_data_transformer_obj()
            
            target_column_name = 'math_score'


            input_feature_train_df = train_df.drop(columns=[target_column_name], axis=1)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns=[target_column_name], axis=1)
            target_feature_test_df = test_df[target_column_name]
            
            logging.info(
                f"Applying preprocessiong object on training dataframe and testing dataframe."
            )
    
            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)
            
            logging.info("preprocessing done")

            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]

            test_arr = np.c_[
                input_feature_test_arr, np.array(target_feature_test_df)
            ]

            logging.info(f'Saving preproccessing object')

            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj =preprocessing_obj
            )

            return(
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )

        except Exception as e:
            raise CustomException(e, sys)