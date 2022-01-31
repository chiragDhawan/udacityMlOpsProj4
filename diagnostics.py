import pandas as pd
import numpy as np
import timeit
import os
import json
import pickle
import subprocess

##################Load config.json and get environment variables
import ingestion
import training

with open('config.json','r') as f:
    config = json.load(f) 

dataset_csv_path = os.path.join(config['prod_deployment_path'],'finaldata.csv')
test_data_path = os.path.join(config['test_data_path'], 'testdata.csv')
deployed_model_path = os.path.join(config['prod_deployment_path'], 'lr_model.pkl')
numeric_columns = ['lastmonth_activity', 'lastyear_activity', 'number_of_employees']

##################Function to get model predictions
def model_predictions(test_path_to_csv):
    #read the deployed model and a test dataset, calculate predictions
    trained_model = pickle.load(open(deployed_model_path , 'rb'))
    test_data = pd.read_csv(test_path_to_csv)
    test_data.pop('corporation')
    test_data.pop('exited')
    x_test = test_data
    y_pred = trained_model.predict(x_test)
    return y_pred

##################Function to get summary statistics
def helper_summary(df:pd.DataFrame, col):
    return [col, df[col].mean(), df[col].median(), df.mode()[col][0]]

def dataframe_summary_na():
    train_data = pd.read_csv(dataset_csv_path)
    nas = list(train_data.isna().sum())
    napercents = [nas[i] / len(train_data.index) for i in range(len(nas))]
    return napercents

def dataframe_summary():
    #calculate summary statistics here
    statistics_list = []
    train_data = pd.read_csv(dataset_csv_path)
    for cols in numeric_columns:
        statistics_list.append(helper_summary(train_data, cols))
    print("summary statistics {}".format(statistics_list))
    return statistics_list #return value should be a list containing all summary statistics

##################Function to get timings
def execution_time():
    #calculate timing of training.py and ingestion.py
    starttime = timeit.default_timer()
    os.system('python training.py')
    timing_training = timeit.default_timer() - starttime
    starttime = timeit.default_timer()
    os.system('python ingestion.py')
    timing_ingestion = timeit.default_timer() - starttime
    return [timing_training, timing_ingestion]

##################Function to check dependencies
def outdated_packages_list():
    #get a list of
    broken = subprocess.check_output(['pip', 'check'])
    installed = subprocess.check_output(['pip', 'list'])
    return broken, installed

if __name__ == '__main__':
    model_predictions(test_data_path)
    dataframe_summary()
    execution_time()
    out_list = outdated_packages_list()
    print(out_list)




    
