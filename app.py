import sys
import os
from Network_security.constants.training_pipeline import DATA_INGESTION_DATABASE_NAME,DATA_INGESTION_COLLECTION_NAME
import certifi
ca= certifi.where()
from Network_security.pipeline.training_pipeline import TrainingPipeline
from dotenv import load_dotenv
from Network_security.pipeline.predication_pipeline import PredicationPipeline
load_dotenv()
mongo_db_url= os.getenv("MONGO_DB_URL")
import pymongo
from Network_security.exceptions import custom_exception
from Network_security.logging.logger import logging
from fastapi import FastAPI,File,UploadFile,Request
from uvicorn import run as app_run
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd 
from Network_security.utils.main_utils.utils import load_object
from fastapi.templating import Jinja2Templates

    # Define the path to your templates directory
template_dir = './templates' 

    # Create a Jinja2 environment


    # Load your template
template = Jinja2Templates(directory='./templates')

client= pymongo.MongoClient(mongo_db_url,tlsCaFile=ca)
database= client[DATA_INGESTION_DATABASE_NAME]
collection= client[DATA_INGESTION_COLLECTION_NAME]
app =FastAPI()
origins=['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

@app.get("/",tags=['authentication'])
async def index():
    return RedirectResponse(url='/docs')
@app.get("/train")
async def train():
    training_pipeline =TrainingPipeline()
    training_pipeline.start_training_pipeline()
    return Response("Training successful!")
@app.post("/predict")
async def predict(request:Request,file: UploadFile = File(...)):
     df= pd.read_csv(file.file)
     df=df.drop('Result',axis=1)
     print(df.columns)
     
     predication_pipelion= PredicationPipeline()
     predication=predication_pipelion.predict_data(df)
     df['predication_column']=predication
     df.to_csv("predication_output/output.csv")
     table_html=df.to_html(classes='table table-striped')
     return template.TemplateResponse("table.html",{'request':request,'table':table_html})
if __name__ =="__main__":
    app_run(app,host="localhost",port=8080)