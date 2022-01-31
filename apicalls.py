import json
import os
import requests

#Specify a URL that resolves to your workspace
URL = "http://127.0.0.1:8000/"

with open('config.json','r') as f:
    config = json.load(f)

test_data_path = os.path.join(config['test_data_path'], 'testdata.csv')

#Call each API endpoint and store the responses
response1 = requests.post(URL+"prediction", json.dumps({"test_data_path":test_data_path}))#put an API call here
response2 = requests.get(URL+"scoring")#put an API call here
response3 = requests.get(URL+"summarystats")#put an API call here
response4 = requests.get(URL+"diagnostics")#put an API call here

#combine all API responses
responses = "prediction {}\n scoring {}\n summarystats {}\n diagnostics {} \n".format(response1.json(),response2.json(),response3.json(),response4.json())#combine reponses here

#write the responses to your workspace
f = open('apireturns.txt','w').write(responses)


