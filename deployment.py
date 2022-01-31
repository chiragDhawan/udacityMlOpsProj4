from flask import Flask, session, jsonify, request
import pandas as pd
import numpy as np
import pickle
import os
import shutil
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import json



##################Load config.json and correct path variable
with open('config.json','r') as f:
    config = json.load(f) 


prod_deployment_path = os.path.join(config['prod_deployment_path']) 
dataset_csv_path = os.path.join(config['output_folder_path'],'finaldata.csv')

####################function for deployment
def store_model_into_pickle(model):
    #copy the latest pickle file, the latestscore.txt value, and the ingestfiles.txt file into the deployment directory
    # copy trained model
    shutil.copyfile(model, prod_deployment_path+'/lr_model.pkl')
    # copy f1 score file
    shutil.copyfile('latestscore.txt', prod_deployment_path+'/latestscore.txt')
    # copy ingestfiles.txt
    shutil.copyfile(dataset_csv_path, prod_deployment_path+'/finaldata.csv')
        
        
if __name__=='__main__':
    model_file = os.path.join(config['output_model_path'], 'lr_model.pkl')
    store_model_into_pickle(model_file)
