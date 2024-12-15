import mysql.connector
from mysql.connector import Error

try:
    connection = mysql.connector.connect(
        host='localhost',
        database='lipsync',
        user='root',
        password=''  # default is no password
    )
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print(f"Connected to MySQL Server version {db_Info}")
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print(f"You're connected to database: {record}")

except Error as e:
    print(f"Error while connecting to MySQL: {e}")
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
