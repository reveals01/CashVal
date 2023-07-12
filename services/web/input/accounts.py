import pandas as pd
import requests
from faker import Faker
import random
from datetime import datetime
import json
import pandas as pd


def generate_account(fake, clients_ids):
    account_data = {
        "bankName": fake.company(),  # This line is updated to generate a random company name
        "clientKey": random.choice(clients_ids),
        "currency": fake.currency_code(),
        "accountName": fake.name(),
        "iban": fake.iban(),
        "bic": fake.bban(),
        "key": fake.iban(),
        "creationDate": fake.date_time_this_month().strftime("%d/%m/%Y %H:%M:%S"),
        "openingDate": fake.date_time_this_month().strftime("%d/%m/%Y %H:%M:%S"),
        "lastUpdate": fake.date_time_this_month().strftime("%d/%m/%Y %H:%M:%S")
    }
    return account_data



def generate_accounts(num_accounts):
    fake = Faker()

    # Load client keys from 'clients.xlsx'
    df_clients = pd.read_excel("clients.xlsx")
    clients_ids = df_clients['key'].to_list()
    accounts_data_list=[]
    for _ in range(num_accounts):
        client_key = random.choice(clients_ids)
        client_business = df_clients[df_clients['key'] == client_key]['business'].values[0]

        # Load user dataframe and filter it based on the business of the client
        user_df = pd.read_excel("users.xlsx")
        user_df = user_df[user_df['business'] == client_business]

        # Get the officers and validators
        officers = user_df[user_df['role'] == 'Officer']['key'].tolist()
        senior_officers = user_df[user_df['role'] == 'Senior Officer']['key'].tolist()

        # Get random officer and validator for each account
        officer_key = random.choice(officers)
        validator_key = random.choice(senior_officers)

        iban=fake.iban()
        account_data = {
        "bankName": 'Bank ' + fake.company(),  # This line is updated to generate a random company name
        "clientKey": random.choice(clients_ids),
        "currency": fake.currency_code(),
        "accountName": 'Acc ' + fake.name(),
        "iban": iban,
        "bic": fake.bban(), 
        "key": iban,
        "officerKey": officer_key,
        "validatorKey": validator_key,
        "creationDate": fake.date_time_this_month().strftime("%d/%m/%Y %H:%M:%S"),
        "openingDate": fake.date_time_this_month().strftime("%d/%m/%Y %H:%M:%S"),
        "lastUpdate": fake.date_time_this_month().strftime("%d/%m/%Y %H:%M:%S")
        }
        accounts_data_list.append(account_data)
    # API endpoint
    URL='http://localhost:5005/api/setaccounts'
    
    # Sending POST request
    r = requests.post(url = URL, json = json.dumps(accounts_data_list))

    # Check status of the request
    if r.status_code == 200:
        # Convert list of dicts to dataframe
        df_accounts = pd.DataFrame(accounts_data_list)
    
        # Write dataframe to excel
        df_accounts.to_excel("accounts.xlsx", index=False)

        print(f"Successfully created {num_accounts} accounts and saved to 'accounts.xlsx'.")
    else:
        print(f"Failed to create accounts. Status code: {r.status_code}.")



if __name__ == "__main__":
    num_accounts = 75
    generate_accounts(num_accounts)