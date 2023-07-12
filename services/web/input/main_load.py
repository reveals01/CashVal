from users import generate_users
from clients import generate_clients
from accounts import generate_accounts
from movements import generate_movements

def main():
    businesses = ['Real Estate', 'PJ', 'Funds of funds', 'PE&DEBT']
    generate_users(businesses)

    generate_clients(businesses)

    num_accounts = 75
    generate_accounts(num_accounts)

    num_movements = 1000
    generate_movements(num_movements)



if __name__ == "__main__":
    main()