from flask import Flask, request, make_response
import logging
import mysql.connector
from datetime import datetime
import socket
import uuid

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

    # Getting the SRV_ID from the cookie, if not present we set it to the server's IP address
    srv_id = request.cookies.get("srv_id")
    if not srv_id:
        srv_id = socket.gethostbyname(socket.gethostname())  # Using the server's IP

    # Removing the port if it exists
    srv_id_display = srv_id.split(":")[0] if ":" in srv_id else srv_id

    # Incrementing the counter in the `global_counter` table
    cursor.execute('UPDATE global_counter SET count = count + 1 WHERE id = 1')
    conn.commit()

    # Getting the updated counter value
    cursor.execute('SELECT count FROM global_counter WHERE id = 1')
    counter = cursor.fetchone()[0]

    # Creating a response with the `srv_id` **without the port**
    response = make_response(f"Hey, your Server srv_id is: {srv_id_display}<br>Counter: {counter}")
    response.set_cookie('srv_id', srv_id)  # Saving the srv_id in the cookie

    # Storing logs in the database
    client_ip = request.remote_addr
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('INSERT INTO access_log (timestamp, client_ip, server_ip) VALUES (%s, %s, %s)', (timestamp, client_ip, srv_id))
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
