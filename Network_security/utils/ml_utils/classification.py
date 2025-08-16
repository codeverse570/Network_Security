from sklearn.metrics import f1_score,recall_score,precision_score
from Network_security.exceptions import custom_exception
from Network_security.entity.artifact_config import ClassificationMetricArtifact
import sys
def classification_metric(y_true,y_predict):
    try:
       return ClassificationMetricArtifact(f1_score=f1_score(y_true,y_predict),precision_score=precision_score(y_true,y_predict),recall_score=recall_score(y_true,y_predict))
    except Exception as e:
          custom_exception(e,sys)