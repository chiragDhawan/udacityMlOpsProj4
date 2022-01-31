import pandas as pd
import numpy as np
import os
import json
from datetime import datetime


#############Load config.json and get input and output paths
with open('config.json','r') as f:
    config = json.load(f) 

input_folder_path = config['input_folder_path']
output_folder_path = config['output_folder_path']

# Function for data ingestion
def merge_multiple_dataframe():
    f_record = open(output_folder_path+"/ingestedfiles.txt",'w')
    allrecords = []
    final_dataframe = pd.DataFrame(columns=['corporation', 'lastmonth_activity' ,'lastyear_activity','number_of_employees','exited'])
    #check for datasets, compile them together, and write to an output file
    for filename in os.listdir(os.getcwd()+'/'+input_folder_path):
        currentdf = pd.read_csv(os.path.join(*[os.getcwd(), input_folder_path, filename]))
        dateTimeObj = datetime.now()
        thetimenow = str(dateTimeObj.year) + '/' + str(dateTimeObj.month) + '/' + str(dateTimeObj.day)
        allrecords.append([input_folder_path, filename, len(currentdf.index), thetimenow])
        final_dataframe = final_dataframe.append(currentdf).reset_index(drop=True)
    final_dataframe.drop_duplicates().to_csv(output_folder_path+'/finaldata.csv',index=False)
    for element in allrecords:
        f_record.write(str(element)+'\n')


if __name__ == '__main__':
    merge_multiple_dataframe()
