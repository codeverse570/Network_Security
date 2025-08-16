import pickle
import sys
import yaml
from sklearn.metrics import r2_score
from Network_security.exceptions import custom_exception
from Network_security.logging.logger import logging
import os
import numpy as np
from sklearn.model_selection import GridSearchCV

def load_yaml_file(file_path):
    try:
        with open(file_path, 'r') as file:
            # Using FullLoader for general purpose, consider SafeLoader for untrusted sources
            data = yaml.safe_load(file)
        
        return data
        # You can access elements like a dictionary or list
        

    except FileNotFoundError as e:
     raise custom_exception(e,sys)
    except yaml.YAMLError as e:
     raise custom_exception(e,sys)

def write_yaml_file(file_path,content):
  try:
   os.makedirs(os.path.dirname(file_path),exist_ok=True)
   with open(file_path, 'w') as file:
    yaml.dump(content, file, sort_keys=False)

  except Exception as e:
     raise custom_exception(e,sys)

def save_array_file(file_path,array):
  try:
    print(array)
    os.makedirs(os.path.dirname(file_path),exist_ok=True)
    np.save(file_path,array)
  except Exception as e:
      raise custom_exception(e,sys)

def save_object(file_path,object):
   try:
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path, 'wb') as file:
            pickle.dump(object, file)
   except Exception as e:
       raise custom_exception(e,sys)
def load_object(file_path):
   try:
      with open(file_path, 'rb') as file:
           return  pickle.load(file)
   except Exception as e:
       raise custom_exception(e,sys)
def load_array_file(file_path):
  try:
    return np.load(file_path)
  except Exception as e:
      raise custom_exception(e,sys)

def evalute_models(x_train,y_train,x_test,y_test,models,params):
  try:
     report={}
     for model in models:
        modelKey=model
        param= params[model]
        model= models[model]
        grid_cv= GridSearchCV(model,param,cv=3)
        grid_cv.fit(x_train,y_train)
        grid_cv.best_params_
        model.set_params(**grid_cv.best_params_)
        model.fit(x_train,y_train)
        y_pred=model.predict(x_test)
        score= r2_score(y_test,y_pred)
        report[modelKey]=score
     return report
  except Exception as e:
      raise custom_exception(e,sys)   