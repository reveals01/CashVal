import os
import pandas as pd
import requests


df = pd.read_excel('./instruments.xlsx')
js_input=df.to_json(orient='records')

# api-endpoint
URL = "http://127.0.0.1:5001/api/setinstruments"

# sending get request and saving the response as response object
r = requests.post(url = URL, json = js_input)
  
# extracting data in json format
print(r)