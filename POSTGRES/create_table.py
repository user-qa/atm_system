from SQL_CONNECTIONS import DATABASE

user_table = """
        CREATE TABLE if not exists user_table(
        id Serial, 
        full_name varchar(40) Not Null,
        card_number varchar(16) Not Null Primary Key,
        expiry_date Date Not Null,
        password varchar(4) Not Null,
        balance numeric Not Null, 
        email varchar(40) unique
        )"""

atm_table = """
        CREATE TABLE if not exists atm_table(
        id Serial Primary Key,
        p200 numeric not null,
        p100 numeric not null,
        p50 numeric not null,   
        p20 numeric not null,
        p10 numeric not null,
        p5 numeric not null
        )"""

insertion = "insert into atm_table(p200,p100,p50,p20,p10,p5) values(10,10,10,10,10,10)"
# the insertion is implemented only once and with the creations of the tables;
tables = [user_table, atm_table, insertion]

for i in tables:
    DATABASE.connect(i, 'create')