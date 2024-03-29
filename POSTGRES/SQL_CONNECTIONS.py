import psycopg2 as psql

class DATABASE:
    @staticmethod
    def connect(query, type):
        database = psql.connect(
            database = "atm",
            host = "localhost",
            user = "postgres",
            password = '1605'
        )

        cursor = database.cursor()
        cursor.execute(query)

        if type in ['insert', 'create', 'update', 'alter']:
            database.commit()

        elif type == 'select':
            ans = cursor.fetchall()
            return ans