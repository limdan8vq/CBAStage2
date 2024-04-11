from flask import Flask, jsonify
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

def exec_query(string_query):
    cursor = connection.cursor()
    cursor.execute(string_query)
    results = cursor.fetchall()
    return results

@app.route('/get_data', methods=['GET'])
def get_data(start_date, end_date):
    cursor = connection.cursor()
    sql_str = "SELECT * FROM storedata WHERE transaction_date BETWEEN %s AND %s"
    cursor.execute(sql_str, (start_date, end_date))
    results = cursor.fetchall()
    #Return as JSON, list, and pandas Data Frame
    return (jsonify(results), results, pd.DataFrame(results))

@app.route('/add_data', methods=['POST'])
def add_data(add_id, add_store_id, add_total_sales, add_date):
    cursor = connection.cursor()
    sql_str = "INSERT INTO sales (id, store_code, total_sale, transaction_date) \
                VALUES (%s, %s, %s, %s)"
    cursor.execute(sql_str, (add_id, add_store_id, add_total_sales, add_date))
    connection.commit()
    sql_str = "SELECT * FROM storedata WHERE id = %s"
    cursor.execute(sql_str, add_id)
    new_row = cursor.fetchall()
    print(new_row)
    return jsonify({'message': 'Data added successfully'})

def close_connection():
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")

if __name__ == '__main__':
    app.run()