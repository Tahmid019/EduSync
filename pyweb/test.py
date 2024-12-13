import mysql.connector
conn = mysql.connector.connect(host='localhost', user='root', password='', database='lipsync')

if conn.is_connected():
    print("Connection is established")
else:
    print("Connection is not established")