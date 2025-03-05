from flask import Flask, request, make_response
import logging
import mysql.connector
from datetime import datetime
import socket

app = Flask(__name__)

# Setting up logging
logging.basicConfig(filename='/logs/app.log', level=logging.INFO)
logger = logging.getLogger()

# Database connection
def get_db_connection():
    conn = mysql.connector.connect(
        host='db',
        user='root',
        password='root',
        database='mydb'
    )
    return conn

# Route "/"
@app.route('/')
def home():
    # Connecting to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Getting the server's IP address
    server_ip = socket.gethostbyname(socket.gethostname())

    # Creating a cookie with the internal IP
    response = make_response(f"Hey, you're Server IP is: {server_ip}")
    response.set_cookie('internal_ip', server_ip)
    
    # Saving logs to the database
    client_ip = request.remote_addr
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('INSERT INTO access_log (timestamp, client_ip, server_ip) VALUES (%s, %s, %s)', (timestamp, client_ip, server_ip))
    conn.commit()

    cursor.close()
    conn.close()

    return response


# Route "/showcount"
@app.route('/showcount')
def show_count():
    # Connecting to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Displaying the global counter
    cursor.execute('SELECT count FROM global_counter WHERE id = 1')
    count = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return f"Global counter is {count}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
