import pickle
from sklearn.metrics import confusion_matrix
import pandas as pd
import numpy as np
from sklearn import metrics
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os



###############Load config.json and get path variables
with open('config.json','r') as f:
    config = json.load(f) 

dataset_csv_path = os.path.join(config['output_folder_path']) 
deployed_model_path = os.path.join(config['prod_deployment_path'], 'lr_model.pkl')
test_data_path = os.path.join(config['test_data_path'], 'testdata.csv')

##############Function for reporting
def score_model():
    #calculate a confusion matrix using the test data and the deployed model
    #write the confusion matrix to the workspace
    # confusion matrix
    trained_model = pickle.load(open(deployed_model_path, 'rb'))
    test_data = pd.read_csv(test_data_path)
    test_data.pop('corporation')
    y_test = test_data['exited']
    test_data.pop('exited')
    x_test = test_data
    y_pred = trained_model.predict(x_test)

    matrix = confusion_matrix(y_test, y_pred, labels=[1, 0])
    print('Confusion matrix : \n', matrix)


if __name__ == '__main__':
    score_model()
