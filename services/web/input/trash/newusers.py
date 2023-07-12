import os
import pandas as pd
import requests

df=pd.read_excel('/Users/thomas/Documents/reveals/CLIENTS/MASSENA/Massena_PS/services/web/input/users.xlsx') 
js_input=df.to_json(orient='records')

# api-endpoint
URL = "http://127.0.0.1:5001/api/setusers"



# defining a params dict for the parameters to be sent to the API
json = js_input
  
# sending get request and saving the response as response object
r = requests.post(url = URL, json = json)
  
# extracting data in json format
print(r)