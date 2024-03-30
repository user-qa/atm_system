from collections import namedtuple

import functions

stop_code = False
while stop_code is False:
    choice = input("""
        1.Register
        2.Login
        3.Admin Page
        4.Stop Code
        
    """)

    if choice == '1':
        full_name = functions.return_full_name()
        card_number = functions.return_card_number()
        expiry_date = functions.return_expiry_date()
        balance = functions.return_balance()
        password = functions.return_password()

        USER = namedtuple('USER', ['full_name', 'card_number', 'expiry_date', 'balance', 'password'])

        user1 = USER(full_name, card_number, expiry_date, balance, password)
        functions.add_user(user1)

        print('Successfully added! ')

    elif choice == '2':

        card_number = functions.return_card_number()
        current_user = functions.check_user_if_available(card_number)
        if current_user is not False:
            full_name = current_user.full_name
            balance = current_user.balance
            expiry_date = current_user.expiry_date
            password = current_user.password

            password_input = functions.return_password()
            if functions.check_password(password, password_input) is True:  # else, just goes back to the main page
                print('Successfully Logged In!')
                log_out = False
                while log_out is False:
                    operation = input("""
                         1. Connect Email
                         2. Balance 
                         3. Withdraw Money
                         4. Replenish the card
                         5. Log Out
                         
                        """)
                    if operation == '1':
                        user_email = functions.return_email(card_number, full_name)
                        if user_email is not None:
                            print(user_email)
                    elif operation == '2':
                        print(functions.return_user_balance(card_number))
                    elif operation == '3':
                        print(functions.withdraw_money(card_number))
                    elif operation == '4':
                        print(functions.add_to_user_balance(card_number))
                    elif operation == '5':
                        log_out = True

    elif choice == '3':
        admin_password = input('Enter the Admin Password: ')
        if admin_password == 'qwerty':
            admin_log_out = False
            while admin_log_out is False:
                admin_operation = input("""
                    1. Insert Money
                    2. ATM Balance
                    3. Log Out  """)
                if admin_operation == '1':
                    # it is not going to add; it is just going to update
                    # if p200 used to be 10, and if I enter 30, it is going to be 30 not 10 + 30 = 40
                    p200 = int(input('Number of 200s: '))
                    p100 = int(input('Number of 100s: '))
                    p50 = int(input('Number of 50s: '))
                    p20 = int(input('Number of 20s: '))
                    p10 = int(input('Number of 10s: '))
                    p5 = int(input('Number of 5s: '))

                    updated_amounts = {
                        '200': p200,
                        '100': p100,
                        '50': p50,
                        '20': p20,
                        '10': p10,
                        '5': p5,
                    }

                    functions.atm_change(updated_amounts)
                    print('Successfully Updated! ')
                elif admin_operation == '2':
                    print(functions.return_atm_balance())
                elif admin_operation == '3':
                    admin_log_out = True

    elif choice == '4':
        break
