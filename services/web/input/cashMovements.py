import pandas as pd
from faker import Faker
import requests
import random
from datetime import datetime, timedelta
import json
from itertools import product

###### enregistrement des users ######
# Set up faker
fake = Faker()
# Define services
businesses = ['Real Estate', 'PJ', 'Funds of funds', 'PE&DEBT']
# Define the number of users for each role
num_users_per_role = {
    'Officer': 20,  # We fill up the rest with Officers
    'Senior Officer': 9,
    'Manager': 4,
    'Director': 2
}

#num_users = 40
#userIds = [fake.unique.email() for i in range(num_users)]
users = []


for role, num_users in num_users_per_role.items():
    for i in range(num_users):
        id=fake.unique.email()
        user = {
            'key':id,
            'email': id,  # Unique email
            'password': fake.password(length=10),  # Fake password
            'name': fake.first_name(),  # Fake name
            'surname': fake.last_name(),  # Fake surname
            'role': role,  # Role as per distribution
            'business': random.choice(businesses),
            'createdDate': datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
            'updatedDate': datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
        }
        users.append(user)

# enregistrement des id users : 
userIds=[u['key'] for u in users]
officerIds=[u['key'] for u in users if u['role']=='Officer']
validatorIds=[u['key'] for u in users if u['role']=='Senior Officer']

# Call the API to create the users
response = requests.post('http://127.0.0.1:5002/api/setusers', json=json.dumps(users))

if response.status_code == 200:
    print('Successfully created users.')
else:
    print(f'Failed to create users. Response: {response.text}')


###### enregistrement des clients ######

# Initialize faker
fake = Faker()

num_clients = 40
def generate_fund_name():
    return f"{fake.company()} {random.choice(['Fund', 'Capital', 'Investments', 'Holdings'])}"

clientsIds=[generate_fund_name() for i in range(num_clients)]

client_data_list = []
for clientId in clientsIds:
    client_data = {
        "key": clientId,
        "email": fake.email(),
        "phone": fake.phone_number(),
        "business":random.choice(businesses),
        "country":fake.country_code(),
        "creationDate": fake.date_time_this_month().strftime("%d/%m/%Y %H:%M:%S")
    }
    client_data_list.append(client_data)

# Send the POST request to the Account API endpoint
URL='http://localhost:5002/api/setclients'
  # sending get request and saving the response as response object
r = requests.post(url = URL, json = json.dumps(client_data_list))
    
# extracting data in json format
print('Clients', r)


###### mise en place de l'organisation ######
fake = Faker()
bank_companies = [fake.company() for _ in range(30)]


#orga_data_list = []
#for clientsId,bank in product(clientsIds,bank_companies):
#    orga_data = {
#        "clientKey": clientsId,
#        "bank": clientsId,
#        "officerKey": random.choice(officerIds), # Select random officer from list
#        "validatorKey": random.choice(validatorIds) # Select random validator from list
#    }
#    orga_data_list.append(orga_data)

# Now, make a POST request to your Flask API
#response = requests.post('http://localhost:5002/api/setorgas', json=json.dumps(orga_data_list))

#if response.status_code == 200:
#    print('Successfully created Orga instances.')
#else:
#    print('Failed to create Orga instances')




# Define the number of clients and accounts
num_accounts = 75
accountIds = [fake.iban() for i in range(num_accounts)]


# Create a list of account data
account_data_list = []
for accountId in accountIds:
    account_data = {
#        "idUser": "",  # random userId from existing ones
        "bankName": random.choice(bank_companies),
        "clientKey": random.choice(clientsIds),
        "currency": fake.currency_code(),
        "accountName": fake.name(),
        "iban": fake.iban(),
        "bic": fake.bban(),
        "key": accountId,
        "creationDate": fake.date_time_this_month().strftime("%d/%m/%Y %H:%M:%S"),
        "openingDate": fake.date_time_this_month().strftime("%d/%m/%Y %H:%M:%S"),
        "lastUpdate": fake.date_time_this_month().strftime("%d/%m/%Y %H:%M:%S")
    }
    account_data_list.append(account_data)

# Send the POST request to the Account API endpoint
URL='http://localhost:5002/api/setaccounts'
  # sending get request and saving the response as response object
r = requests.post(url = URL, json = json.dumps(account_data_list))
    
# extracting data in json format
print('Accounts', r)



# Set up faker
fake = Faker()

# Create a pandas DataFrame
df = pd.DataFrame(columns=['accountKey', 'movementDate', 'movementValueDate', 'sense', 'amount', 'ctrParName', 'ctrParIban', 'ctrParCountry', 'communication'])

# Populate the DataFrame with fake data
for _ in range(1000):  # Generate 100 records
    accountKey = fake.random_element(elements=accountIds)
    # Generate random date within the last month for movementDate
    start_date = datetime.now() - timedelta(days=5)
    end_date = datetime.now()
    movementDate = fake.date_time_between(start_date=start_date, end_date=end_date).strftime("%d/%m/%Y %H:%M:%S") 

    # movementValueDate is 2 days after movementDate
    movementDate_obj = datetime.strptime(movementDate, "%d/%m/%Y %H:%M:%S")
    movementValueDate_obj = movementDate_obj + timedelta(days=2)
    movementValueDate = movementValueDate_obj.strftime("%d/%m/%Y %H:%M:%S")

    sense = random.choice(['IN', 'OUT'])  # Random choice for sense
    amount = round(random.uniform(1000, 10000000), 2)  # Random float for amount
    ctrParName = fake.name()  # Fake name
    ctrParIban = fake.iban()  # Fake IBAN
    ctrParCountry = fake.country_code()  # Fake country code
    communication = fake.bs()  # Fake finance-related text

    # Append the fake data to the DataFrame

    df = pd.concat([df,pd.DataFrame([{
        'accountKey': accountKey,
        'movementDate': movementDate,
        'movementValueDate': movementValueDate,
        'sense': sense,
        'amount': amount,
        'ctrParName': ctrParName,
        'ctrParIban': ctrParIban,
        'ctrParCountry': ctrParCountry,
        'communication': communication,
    }])], ignore_index=True)

json_data = df.to_json(orient='records')
#print('json_data',json_data)
URL='http://localhost:5005/api/cash_movements'
  # sending get request and saving the response as response object
r = requests.post(url = URL, json = json_data)
    
# extracting data in json format
print('Movements', r)



