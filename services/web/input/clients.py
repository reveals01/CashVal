import pandas as pd
import requests
from faker import Faker
import random
from datetime import datetime
import json


def generate_client(fake, business):
    client_data = {
        "key": 'Fund ' + generate_fund_name(fake),
        "email": fake.email(),
        "phone": fake.phone_number(),
        "business": business,
        "country": fake.country_code(),
        "creationDate": fake.date_time_this_month().strftime("%d/%m/%Y %H:%M:%S")
    }
    return client_data

def generate_fund_name(fake):
    return f"{fake.company()} {random.choice(['Fund', 'Capital', 'Investments', 'Holdings'])}"

def generate_clients(businesses):
    # Initialize faker
    fake = Faker()

    num_clients = 40
    client_data_list = []

    # Generate client data
    for _ in range(num_clients):
        client_data_list.append(generate_client(fake, random.choice(businesses)))

    # Call the setclients API
    response = requests.post('http://localhost:5005/api/setclients', json=json.dumps(client_data_list))
    if response.status_code == 200:
        print("Clients added successfully!")
    else:
        print(f"Failed to add clients, status code: {response.status_code}")

        # Create pandas DataFrame and save to Excel
    df = pd.DataFrame(client_data_list)
    df.to_excel('clients.xlsx', index=False)
    print("Data saved to user.xlsx")

    return client_data_list



if __name__ == "__main__":
    businesses = ['Real Estate', 'PJ', 'Funds of funds', 'PE&DEBT']
    clients = generate_clients(businesses)
