from flask import Flask, render_template, request, jsonify
import mysql.connector
from mysql.connector import Error
from datetime import date
import pandas as pd

app = Flask(__name__)

try:
    connection = mysql.connector.connect(host='localhost',
                                         database='storedata',
                                         user='root',
                                         password='BobLives@House2023')
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to databse: ", record)

except Error as e:
    print("Error while connecting to MySQL", e)

# finally:
#     if connection.is_connected():
#         cursor.close()
#         connection.close()
#         print("MySQL connection is closed")

def exec_query(string_query):
    cursor = connection.cursor()
    cursor.execute(string_query)
    results = cursor.fetchall()
    # print("You're connected to databse: ", record)
    return results

@app.route('/get_data', methods=['GET'])
def get_data(start_date, end_date):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM storedata WHERE transaction_date BETWEEN start_date AND end_date", (start_date, end_date))
    results = cursor.fetchall()
    #Return as JSON, list, and pandas Data Frame
    return (jsonify(results), results, pd.DataFrame(results))

@app.route('/add_data', methods=['POST'])
def add_data(add_id, add_store_id, add_total_sales, add_date):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO storedata (id, store_code, total_sale, transaction_date) VALUES (add_id, add_store_id, add_total_sales, add_date)", (add_id, add_store_id, add_total_sales, add_date))
    

@app.route('/hello')
def hello_world():
    return 'Hello World! My name is Daniel!'

def close_connection():
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")

if __name__ == '__main__':
    app.run()