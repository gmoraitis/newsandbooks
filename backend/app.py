from flask import Flask, request, jsonify, session
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
app.config.from_object('config.Config')
CORS(app)

def get_db_connection():
    conn = psycopg2.connect(
        dbname="news_books_db",
        user="postgres",
        password="8281",  # leave empty if no password
        host="localhost"
    )
    return conn

@app.route('/')
def index():
    return "Welcome to News&Books!"

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    name = data.get('name')
    password = data.get('password')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE name = %s AND password = %s", (name, password))
    user = cursor.fetchone()

    if not user:
        return jsonify({'message': 'Please use correct name and password'}), 401

    cursor.execute("SELECT roles.name FROM roles "
                   "JOIN user_roles ON roles.id = user_roles.role_id "
                   "WHERE user_roles.user_id = %s", (user[0],))
    roles = cursor.fetchall()

    session['user'] = name
    if any(role[0] == 'premium_access' for role in roles):
        return jsonify({'access': 'premium', 'products': ['Todays News', 'News Around the World', 'Book 1', 'Book 2']})
    else:
        return jsonify({'access': 'limited', 'products': ['Todays News', 'News Around the World']})

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return jsonify({'message': 'Logged out successfully'})

if __name__ == '__main__':
    app.run(debug=True)
