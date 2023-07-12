import os
import pandas as pd
import requests
from faker import Faker
import requests
import random
from datetime import datetime
import json

def newParameters():
    # get file
    df = pd.read_excel('./produitStructure.xlsx',sheet_name='Autocall')
    
    def newParameterTable(df,col,name):
        res=pd.DataFrame()
        x=df[col].fillna('NONE')
        res['label']=[y.strip().upper() for y in x.unique()]
        res['typeLabel']=name
        return res
    
    df_res_1=newParameterTable(df,'Type','produit')
    df_res_2=newParameterTable(df,'clientele_cible','clientele')
    df_res_3=newParameterTable(df,'Emetteur','emetteur')
    df_res_4=newParameterTable(df,'typePanier','panier')
    df_res_5=newParameterTable(df,'Capital garanti','protection')
    df_res_6=newParameterTable(df,'Type de barrière','barriere')
    df_res_7=newParameterTable(df,'Remuneration','remuneration')
    df_res_8=newParameterTable(df,'Coupon ou Participation','garantie')
    df_res_9=newParameterTable(df,'Type de produit','produit2')
    df_res_10=newParameterTable(df,'Devise','devise')
    df_res_11=newParameterTable(df,'Periode','periodeRemb')

    df_res_tot=pd.concat([df_res_1,df_res_2,df_res_3,df_res_4,df_res_5,df_res_6,df_res_7,df_res_8,df_res_9,df_res_10,df_res_11])

    json_data = df_res_tot.to_json(orient='records')
    
    # api-endpoint
    URL = "http://127.0.0.1:5002/api/setparameters"

    # sending get request and saving the response as response object
    r = requests.post(url = URL, json = json_data)
    
    # extracting data in json format
    print('Parameters', r)



# Set up faker
fake = Faker()

# Define services
services = ['Real Estate', 'PJ', 'Funds of funds', 'PE&DEBT']

# Define the number of users for each role
num_users_per_role = {
    'Officer': 9,  # We fill up the rest with Officers
    'Senior Officer': 15,
    'Manager': 4,
    'Director': 2
}

# Generate users
def newUsers2():
    users = []
    for role, num_users in num_users_per_role.items():
        for _ in range(num_users):
            user = {
                'idUser': fake.unique.random_number(digits=5),  # Unique ID
                'fk': fake.random_number(digits=5),  # Fake FK
                'email': fake.unique.email(),  # Unique email
                'password': fake.password(length=10),  # Fake password
                'name': fake.first_name(),  # Fake name
                'role': role,  # Role as per distribution
                'group': fake.word(),  # Fake group
                'surname': fake.last_name(),  # Fake surname
                'createdDate': datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                'updatedDate': datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                'service': random.choice(services),  # Random service
            }
            users.append(user)

    # Call the API to create the users
    response = requests.post('http://127.0.0.1:5002/api/setusers', json=json.dumps(users))

    if response.status_code == 200:
        print('Successfully created users.')
    else:
        print(f'Failed to create users. Response: {response.text}')







def initLoad():
    newParameters()
    newUsers2()
    

if __name__ == "__main__":
    initLoad()