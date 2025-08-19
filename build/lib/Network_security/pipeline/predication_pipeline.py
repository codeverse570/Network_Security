from Network_security.utils.ml_utils.estimator import NetworkModel

from Network_security.utils.main_utils.utils import load_object
class PredicationPipeline:
    def __init__(self):
        
        pass
    def predict_data(self,data):
        model= load_object('final_model/model.pkl')
        preprocessor= load_object('final_model/processor.pkl')
        network_model=NetworkModel(preprocessor=preprocessor,model=model)
        predication=network_model.predict(data)
        return predication