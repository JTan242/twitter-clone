import argparse
import sqlalchemy
import random
import string

parser = argparse.ArgumentParser()
parser.add_argument('--db', default="postgresql://postgres:pass@postgres:5432")
args = parser.parse_args()

engine = sqlalchemy.create_engine(args.db, connect_args={
    'application_name': 'insert_data.py',
})
connection = engine.connect()

# Define characters for alphanumeric string generation
alphanumeric_chars = string.ascii_letters + string.digits

# Function to generate random alphanumeric strings
def generate_random_alphanumeric(length):
    return ''.join(random.choice(alphanumeric_chars) for _ in range(length))

# Function to generate random users
def generate_users(num_users):
    for i in range(num_users):
        username = generate_random_alphanumeric(10)  # Adjust length as needed
        password = generate_random_alphanumeric(10)  # Adjust length as needed
        sql = sqlalchemy.sql.text("""
        INSERT INTO users (username, password) VALUES (:u, :p);
        """)
        res = connection.execute(sql, {
            'u': username,
            'p': password
        })
        print("User", i)

# Function to generate random URLs
def generate_urls(num_urls):
    for i in range(num_urls):
        url = generate_random_alphanumeric(10)  # Adjust length as needed
        sql = sqlalchemy.sql.text("""
        INSERT INTO urls (url) VALUES (:url);
        """)
        res = connection.execute(sql, {
            'url': url
        })
        print("URL", i)


def generate_tweets(num_tweets):
    # Get the maximum user ID from the users table
    max_user_id = connection.execute("SELECT MAX(id_users) FROM users").scalar()
    
    if max_user_id is None:
        max_user_id = 0
    
    for i in range(num_tweets):
        if max_user_id > 0:
            id_users = random.randint(1, max_user_id)
        else:
            id_users = 1  # Default to 1 if there are no users in the database
        
        text = generate_random_alphanumeric(50)  # Adjust length as needed
        sql = sqlalchemy.sql.text("""
            INSERT INTO tweets (id_users, text) VALUES (:id_users, :text);
        """)
        res = connection.execute(sql, {
            'id_users': id_users,
            'text': text
        })
        print("Tweet", i)

# Call functions to generate data
generate_users(50)
generate_urls(50)
generate_tweets(50)

# Close the connection
connection.close() 

