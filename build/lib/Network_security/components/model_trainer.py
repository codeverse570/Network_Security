from Network_security.utils.ml_utils.classification import classification_metric
from Network_security.utils.ml_utils.estimator import NetworkModel
from Network_security.entity.artifact_config import DataTransformationArtifact,ClassificationMetricArtifact,ModelTrainerArtifact
from Network_security.entity.config_entity import ModelTrainerConfig
from Network_security.utils.main_utils.utils import load_array_file,evalute_models,load_object,save_object
from Network_security.exceptions import custom_exception
from sklearn.linear_model import LogisticRegression
import os
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier,
)
import sys
class ModelTrainer:
    def __init__(self,dataTransformationArtifact:DataTransformationArtifact,modelTrainerConfig:ModelTrainerConfig):
        self.dataTransfromationArtifact= dataTransformationArtifact
        self.modelTrainerConfig=modelTrainerConfig
        pass
    def 
    def train_model(self,x_train,y_train,x_test,y_test):
         
         models = {
                "Random Forest": RandomForestClassifier(verbose=1),
                "Decision Tree": DecisionTreeClassifier(),
                "Gradient Boosting": GradientBoostingClassifier(verbose=1),
                "Logistic Regression": LogisticRegression(verbose=1),
                "AdaBoost": AdaBoostClassifier(),
            }
         params={
            "Decision Tree": {
                'criterion':['gini', 'entropy', 'log_loss'],
                # 'splitter':['best','random'],
                # 'max_features':['sqrt','log2'],
            },
            "Random Forest":{
                # 'criterion':['gini', 'entropy', 'log_loss'],
                
                # 'max_features':['sqrt','log2',None],
                'n_estimators': [8,16,32,128,256]
            },
            "Gradient Boosting":{
                # 'loss':['log_loss', 'exponential'],
                'learning_rate':[.1,.01,.05,.001],
                'subsample':[0.6,0.7,0.75,0.85,0.9],
                # 'criterion':['squared_error', 'friedman_mse'],
                # 'max_features':['auto','sqrt','log2'],
                'n_estimators': [8,16,32,64,128,256]
            },
            "Logistic Regression":{},
            "AdaBoost":{
                'learning_rate':[.1,.01,.001],
                'n_estimators': [8,16,32,64,128,256]
            }
            
        }
         report=evalute_models(x_train,y_train,x_test,y_test,models,params)
         best_model_score= max(report.values())
         best_model_name= max(report,key=report.get)
         best_model= models[best_model_name]
         y_pred_train=best_model.predict(x_train)
         y_pred_test=best_model.predict(x_test)
         classificationMetricTest= classification_metric(y_test,y_pred_test)
         classificationMetricTrain= classification_metric(y_train,y_pred_train)
         preprocessor=  load_object(self.dataTransfromationArtifact.transformed_object_file_path)
         bestModel= NetworkModel(preprocessor,best_model)
         os.makedirs(os.path.dirname(self.modelTrainerConfig.trained_model_file_path),exist_ok=True)
         save_object(self.modelTrainerConfig.trained_model_file_path,bestModel)
         return ModelTrainerArtifact(trained_model_file_path=self.modelTrainerConfig.trained_model_file_path,test_metric_artifact=classificationMetricTest,train_metric_artifact=classificationMetricTrain)

         
         
    
        
    def intiate_model_trainer(self):
         try:
             train_data= load_array_file(self.dataTransfromationArtifact.transformed_train_file_path)
             test_data= load_array_file(self.dataTransfromationArtifact.transformed_test_file_path)
             x_train=train_data[:,:-1]
             y_train= train_data[:,-1]
             x_test= test_data[:,:-1]
             y_test= test_data[:,-1]
             return self.train_model(x_train,y_train,x_test,y_test)
             pass
         
         except Exception as e:
             raise custom_exception(e,sys)