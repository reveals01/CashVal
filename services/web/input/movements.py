import pandas as pd
import requests
from faker import Faker
import random
from datetime import datetime
import json
from datetime import timedelta

def generate_movement(fake, account_ids):
    account_key = fake.random_element(elements=account_ids)
    start_date = datetime.now() - timedelta(days=5)
    end_date = datetime.now()
    movement_date = fake.date_time_between(start_date=start_date, end_date=end_date).strftime("%d/%m/%Y %H:%M:%S")
    
    movement_date_obj = datetime.strptime(movement_date, "%d/%m/%Y %H:%M:%S")
    movement_value_date_obj = movement_date_obj + timedelta(days=2)
    movement_value_date = movement_value_date_obj.strftime("%d/%m/%Y %H:%M:%S")
    
    movement_data = {
        "accountKey": account_key,
        "movementDate": movement_date,
        "movementValueDate": movement_value_date,
        "sense": random.choice(['IN', 'OUT']),
        "amount": round(random.uniform(1000, 10000000), 2),
        "ctrParName": fake.name(),
        "ctrParIban": fake.iban(),
        "ctrParCountry": fake.country_code(),
        "communication": fake.bs(),
    }
    return movement_data

def generate_movements(num_movements):
    fake = Faker()
    
    # Load account keys from 'accounts.xlsx'
    df_accounts = pd.read_excel("accounts.xlsx")
    account_ids = df_accounts['key'].to_list()

    movements_data_list = [generate_movement(fake, account_ids) for _ in range(num_movements)]

    # API endpoint
    URL='http://localhost:5005/api/cash_movements'

    # Sending POST request
    r = requests.post(url = URL, json = json.dumps(movements_data_list))

    # Check status of the request
    if r.status_code == 200:
        # Convert list of dicts to dataframe
        df_movements = pd.DataFrame(movements_data_list)
    
        # Write dataframe to excel
        df_movements.to_excel("movements.xlsx", index=False)

        print(f"Successfully created {num_movements} movements and saved to 'movements.xlsx'.")
    else:
        print(f"Failed to create movements. Status code: {r.status_code}.")


if __name__ == "__main__":
    num_movements = 1000
    generate_movements(num_movements)