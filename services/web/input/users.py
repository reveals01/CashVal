import pandas as pd
import requests
from faker import Faker
import random
from datetime import datetime
import json

def generate_user(fake, role, business):
    id=fake.unique.email()
    user = {
        'key':id,
        'email': id,  # Unique email
        'password': fake.password(length=10),  # Fake password
        'name': fake.first_name(),  # Fake name
        'surname': fake.last_name(),  # Fake surname
        'role': role,  # Role
        'business': business,
        'createdDate': datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
        'updatedDate': datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
    }
    return user

def generate_users(businesses):
    # Initialize faker and empty list of users
    fake = Faker()
    users = []

    # Generate user data
    for business in businesses:
        # Generate 1 Manager
        users.append(generate_user(fake, 'Manager', business))

        # Generate 2 Senior Officers
        for _ in range(2):
            users.append(generate_user(fake, 'Senior Officer', business))

        # Generate 8 Officers
        for _ in range(8):
            users.append(generate_user(fake, 'Officer', business))

    # Generate 2 Directors
    for _ in range(2):
        users.append(generate_user(fake, 'Director', None))

    # Call the setusers API
    response = requests.post('http://127.0.0.1:5005/api/setusers', json=json.dumps(users))
    if response.status_code == 200:
        print("Users added successfully!")
    else:
        print(f"Failed to add users, status code: {response.status_code}")

    # Create pandas DataFrame and save to Excel
    df = pd.DataFrame(users)
    df.to_excel('users.xlsx', index=False)
    print("Data saved to user.xlsx")

    return users







if __name__ == "__main__":
    businesses = ['Real Estate', 'PJ', 'Funds of funds', 'PE&DEBT']
    users = generate_users(businesses)