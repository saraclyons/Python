from mysql.connector import MySQLConnection, Error
from signup_config import read_config

db_config = read_config('mysql')


def insert_user(email, password):
    query = "INSERT INTO users(email,passwd) " \
            "VALUES(%s,%s)"
    args = (email, password)

    try:
        conn = MySQLConnection(**db_config)

        cursor = conn.cursor()
        cursor.execute(query, args)

        conn.commit()
    except Error as error:
        raise Exception(error)

    finally:
        cursor.close()
        conn.close()
