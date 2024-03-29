import random
import smtplib
from collections import namedtuple
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from POSTGRES.SQL_CONNECTIONS import DATABASE


def return_full_name() -> str:
    # Only letters are acceptable here as in full name

    full_name = input('Enter your full name: ')
    return full_name


def return_card_number() -> str:
    # Checks whether all elements are digits and whether len == 16

    card_number = input('Enter your card number: ')
    if card_number.isdigit() and len(card_number) == 16:
        return card_number
    else:
        print('Invalid Card Number! ')
        return return_card_number()


def return_expiry_date():  # Returns a date format

    ed = input('Enter the expiry date [yyyy-mm-dd]: ')
    if ed[:4].isdigit() and ed[5:7].isdigit() and ed[8:10] and ed[4] == ed[7] == '-':
        if check_expiry_date(ed):
            return ed
    print('Invalid Expiry Date! ')
    return return_expiry_date()


def return_password() -> str:
    password = input('Enter the password: ')

    if len(password) == 4:
        if password.isdigit():
            return password
    print('Invalid Password Format! ')
    return return_password()


def return_balance() -> int:
    balance = input('Enter the balance: ')
    if balance.isdigit():
        return int(balance)

    print('Invalid Balance Format! ')
    return return_balance()


def check_expiry_date(date) -> bool:
    # Checks whether the expiry date has passed or not;
    # If passed returns False:

    today_date = datetime.today().date()
    today = datetime.strptime(f'{today_date}', "%Y-%m-%d")
    expiry_date = datetime.strptime(date, "%Y-%m-%d")

    if today < expiry_date:
        return True
    elif today > expiry_date:
        return False


def send_sms(full_name: str, receiver_email: str):
    sender_mail = "qalamochirgich@gmail.com"
    password = "enpdjqayzsxcxqfv"

    message = MIMEMultipart()
    message["From"] = sender_mail
    message["To"] = receiver_email
    message["Subject"] = "Nazarboy's ATM verification"

    code = random.randint(1000, 9999)

    text = f"Diqqat {full_name.upper()}! Email orqali kelgan kodni hech kimga bermang.\n Code: {code}"
    message.attach(MIMEText(text, 'plain'))

    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(sender_mail, password)
        texto = message.as_string()
        connection.sendmail(from_addr=sender_mail, to_addrs=receiver_email, msg=texto)

    return str(code)


def return_email(card_number, full_name, email=None):
    if email is None:
        receiver_email = input('Enter your valid email: ')
    else:
        receiver_email = email
    sent_code = send_sms(full_name, receiver_email)
    n = 1
    while n <= 3:
        ver_code = input('Enter the Verification Code: ')
        if sent_code == ver_code:
            query = f"update user_table set email = '{receiver_email}' where card_number = '{card_number}'"
            DATABASE.connect(query, 'update')
            return 'Successfully Added'
        else:
            print('Wrong Verification Code! ')
    print('Process Failed! ')
    choice = """
        1.Resend the Code
        2.Change Email
        3.Exit
        """
    if choice == '1':
        return return_email(full_name, receiver_email)
    elif choice == '2':
        return return_email(full_name)
    else:
        return None


def return_user_balance(card_number):
    query = f"Select balance from user_table where card_number = '{card_number}'"
    balance = DATABASE.connect(query, 'select')
    return balance[0][0]


def return_atm_cash_each() -> dict:
    query = "select * from atm_table"
    data = DATABASE.connect(query, 'select')
    each_cash_dict = {
        '200': data[0][1],
        '100': data[0][2],
        '50': data[0][3],
        '20': data[0][4],
        '10': data[0][5],
        '5': data[0][6]
    }

    return each_cash_dict


def return_atm_balance() -> int:
    cups_dict = return_atm_cash_each()
    total = sum([int(key) * value for (key, value) in list(cups_dict.items())])
    return total * 1000


def user_balance_change(card_number, amount):
    query = f"update user_table set balance = {amount} where card_number = '{card_number}'"
    DATABASE.connect(query, 'update')


def atm_change(atm_remaining: dict):
    print(atm_remaining)
    query = f"update atm_table set p200 = {atm_remaining['200']},p100 = {atm_remaining['100']},p50 = {atm_remaining['50']},p20 = {atm_remaining['20']},p10 = {atm_remaining['10']},p5 = {atm_remaining['5']} where id = 1"
    DATABASE.connect(query, 'update')


def withdraw_money(card_number: str) -> str:
    cash_to_get = int(input('Amount You Want To Withdraw: '))
    while cash_to_get % 1000 != 0:
        cash_to_get = int(input('Correct Amount You Want To Withdraw: '))
    d = cash_to_get
    cash_to_get //= 1000
    user_balance = return_user_balance(card_number)
    atm_balance = return_atm_balance()

    if cash_to_get < user_balance:
        if cash_to_get < atm_balance:
            each_dict = return_atm_cash_each()
            new_dict_user = {}
            for i in each_dict.keys():
                a = cash_to_get // int(i)
                if each_dict[i] > a:
                    new_dict_user[i] = a
                    cash_to_get %= int(i)
                    each_dict[i] -= a
                else:
                    new_dict_user[i] = each_dict[i]
                    cash_to_get -= int(i) * each_dict[i]
                    each_dict[i] = 0
            if cash_to_get == 0:
                remained_balance_user = user_balance - d
                user_balance_change(card_number, remained_balance_user)
                atm_change(each_dict)

                return 'Get Your Money!!!'

            else:
                return 'Operation Failed'
        else:
            return 'Not Enough ATM Balance'
    else:
        return 'Not Enough Money In Your Balance'


def add_user(user1):
    query = f"INSERT INTO user_table (full_name, card_number, expiry_date, balance, password) values ('{user1.full_name}', '{user1.card_number}', '{user1.expiry_date}','{user1.balance}','{user1.password}') "
    DATABASE.connect(query, 'insert')


def check_user_if_available(card_number: str):
    query = f"select * from user_table where card_number = '{card_number}'"
    data = DATABASE.connect(query, 'select')
    if data is None:
        return False
    else:
        USER = namedtuple('USER', ['full_name', 'card_number', 'expiry_date', 'password', 'balance'])
        current_user = USER(data[0][1], data[0][2], data[0][3], data[0][4], data[0][5])
        return current_user


def check_password(valid_password, entered_password):
    if valid_password == entered_password:
        return True
    else:
        for i in range(2):
            entered_password = input('Enter the password: ')
            if valid_password == entered_password:
                return True
        return False
