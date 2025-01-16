##   Check Connection to MySQL Database
import mysql.connector
import pandas as pd
# Database connection details
# Connect to MySQL Database
try:
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='0123456789',
        database='cameroon_agric'
    )
    cursor = conn.cursor()
    print("Connected to the database.")

except mysql.connector.Error as e:
    print(f"Error while connecting to MySQL: {e}")

finally:
    if conn.is_connected():
        cursor.close()
        conn.close()
        print("MySQL connection is closed.")