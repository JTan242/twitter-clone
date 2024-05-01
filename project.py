from flask import Flask, render_template, request, make_response, redirect, url_for
import psycopg2
from datetime import datetime
import argparse

app = Flask(__name__)

# PostgreSQL database connection configuration
db_config = {
    'dbname': 'your_database_name',
    'user': 'your_username',
    'password': 'your_password',
    'host': 'localhost',
    'port': '5432'  # Default PostgreSQL port
}

# Function to check if credentials are good (You need to define this function)
def are_credentials_good(username, password, db_connection):
    try:
        cur = db_connection.cursor()
        sql = "SELECT username, password FROM users WHERE username = %s;"
        cur.execute(sql, (username,))
        result = cur.fetchone()
        if result and result[1] == password:
            return True
        else:
            return False
    except psycopg2.Error as e:
        print("Error checking credentials:", e)
        return False




@app.route('/')
def root():
    messages = []
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()
    sql = 'SELECT sender_id, message, created_at FROM messages ORDER BY created_at DESC'
    cur.execute(sql)
    for row_messages in cur.fetchall():
        sql = 'SELECT username, age FROM users WHERE id=%s;'
        cur.execute(sql, (row_messages[0],))
        row_users = cur.fetchone()
        if row_users:
            messages.append({
                'message': row_messages[1],
                'created_at': row_messages[2],
                'username': row_users[0],
                'profpic': 'https://robohash.org/' + row_users[0],  # Assuming this URL is correct
                'age': row_users[1]
            })
    cur.close()
    conn.close()
    
    # Check if logged in correctly
    username = request.cookies.get('username')
    password = request.cookies.get('password')
    good_credentials = are_credentials_good(username, password)
    return render_template('root.html', messages=messages, good_credentials=good_credentials, logged_in=False)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()
        cur.execute('''
            SELECT username, password FROM users WHERE username=%s AND password=%s;
        ''', (username, password))
        row = cur.fetchone()
        cur.close()
        conn.close()
        if row:
            res = make_response(redirect(url_for('root')))
            res.set_cookie('username', username)
            res.set_cookie('password', password)
            return res
        else:
            return render_template('login.html', login_unsuccessful=True)
    return render_template('login.html', login_default=True)

@app.route('/logout')
def logout():
    response = make_response(render_template('logout.html'))
    response.set_cookie('username', '', expires=0)
    response.set_cookie('password', '', expires=0)
    return response

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        age = request.form.get('age')
        if password1 != password2:
            return render_template('create_user.html', successful=False, wrongPass=True)
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()
        try:
            cur.execute('''
                INSERT INTO users (username, password, age) VALUES (%s, %s, %s);
            ''', (username, password1, age))
            conn.commit()
            return make_response(render_template('create_user.html', successful=True))
        except psycopg2.IntegrityError:
            return render_template('create_user.html', taken=True, username=username)
        finally:
            cur.close()
            conn.close()
    return render_template('create_user.html')

@app.route('/create_message', methods=['POST'])
def create_message():
    username = request.cookies.get('username')
    password = request.cookies.get('password')
    good_credentials = are_credentials_good(username, password)
    if good_credentials and request.form.get('newmessage'):
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()
        try:
            cur.execute('''
                SELECT id FROM users WHERE username=%s;
            ''', (username,))
            user_id = cur.fetchone()[0]
            now = datetime.now()
            dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
            cur.execute('''
                INSERT INTO messages (sender_id, message, created_at) VALUES (%s, %s, %s);
            ''', (user_id, request.form.get('newmessage'), dt_string))
            conn.commit()
            return make_response(render_template('create_message.html', created=True, username=username, password=password))
        except:
            conn.rollback()
            print("An error occurred while creating the message.")
        finally:
            cur.close()
            conn.close()
    return make_response(render_template('create_message.html', created=False, username=username, password=password))

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_query = request.form.get('search')
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()
        try:
            cur.execute('''
                SELECT users.username, messages.message, messages.created_at, messages.id 
                FROM messages 
                JOIN users ON messages.sender_id = users.id
                WHERE messages.message ILIKE %s;
            ''', ('%' + search_query + '%',))
            rows = cur.fetchall()
            messages = [{'username': row[0], 'text': row[1], 'created_at': row[2], 'id': row[3]} for row in rows]
            messages.reverse()
            return render_template('search_message.html', messages=messages, username=request.cookies.get('username'), password=request.cookies.get('password'))
        except Exception as e:
            print("An error occurred while searching:", e)
        finally:
            cur.close()
            conn.close()
    return render_template('search_message.html', default=True, username=request.cookies.get('username'), password=request.cookies.get('password'))

if __name__ == '__main__':
    app.run(host="0.0.0.0")

