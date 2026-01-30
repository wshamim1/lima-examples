from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/fetch', methods=['GET'])
def fetch():
    conn = mysql.connector.connect(
        host='mysql',
        user='example_user',
        password='example_password',
        database='example_db'
    )
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), email VARCHAR(255))")
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('form.html', users=users)

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    # Connect to MySQL
    conn = mysql.connector.connect(
        host='mysql',
        user='example_user',
        password='example_password',
        database='example_db'
    )
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), email VARCHAR(255))")
    cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
    conn.commit()
    cursor.close()
    conn.close()
    return f"Received and saved: {name}, {email}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
