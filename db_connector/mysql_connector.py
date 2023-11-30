import mysql.connector

__connection = None


def mysql_connection():
    global __connection
    if __connection is None:
        __connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="grocery_store",
            port="3307"
        )

    if __connection.is_connected():
        print("Connected to MySQL database")
        return __connection
    else:
        print("Failed to connect to MySQL database")
        return None
