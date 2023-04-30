import mysql.connector
import jsonify

# Configure the MySQL database connection
db_config = {
    'host': 'mars.cxmpute.com',
    'port': 3306,
    'user': 'u174_Y3pY5Tq1cm',
    'password': 'ZN5y!HNp.Un=uUYnQrWZzg0Y',
    'database': 's174_in-game-currency-management'
}

# Define the function for getting the user's balance
def get_balance(username):
    # Establish a connection to the database
    conn = mysql.connector.connect(**db_config)

    # Use the connection to execute an SQL query to select the user's balance
    with conn.cursor() as cursor:
        cursor.execute('SELECT Cash FROM user WHERE username = %s', (username,))
        result = cursor.fetchone()

    # Close the connection
    conn.close()

    # Return the user's balance
    return result[0]

# Define the function for getting the user's admin status
def get_admin_status(username):
    # Establish a connection to the database
    conn = mysql.connector.connect(**db_config)

    # Use the connection to execute an SQL query to select the user's admin status
    with conn.cursor() as cursor:
        cursor.execute('SELECT Admin FROM user WHERE username = %s', (username,))
        result = cursor.fetchone()

    # Close the connection
    conn.close()

    # Return a boolean indicating the user's admin status
    return bool(result[0])

# Function for password-only login
def login(password):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM user WHERE password = %s', (password,))
    user = cursor.fetchone()
    cursor.close()
    connection.close()

    if user:
        # Return the user's cash balance and admin status
        return {'balance': user[2], 'admin': user[3], 'username': user[1]}
    else:
        return {'error': 'Invalid password'}

# Function for adding cash to a user's account
def add_cash(password, amount):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM user WHERE password = %s', (password,))
    user = cursor.fetchone()

    if user:
        # Add the specified amount of cash to the user's account
        new_balance = user[2] + int(amount)
        cursor.execute('UPDATE user SET Cash = %s WHERE password = %s', (new_balance, password))
        connection.commit()
        cursor.close()
        connection.close()
        return {'message': 'Cash added successfully', 'new_balance': new_balance}
    else:
        cursor.close()
        connection.close()
        return {'error': 'Invalid password'}

# Function for deducting cash from a user's account
def deduct_cash(password, amount):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM user WHERE password = %s', (password,))
    user = cursor.fetchone()

    if user:
        # Deduct the specified amount of cash from the user's account
        new_balance = user[2] - int(amount)
        if new_balance >= 0:
            cursor.execute('UPDATE user SET Cash = %s WHERE password = %s', (new_balance, password))
            connection.commit()
            cursor.close()
            connection.close()
            return {'message': 'Cash deducted successfully', 'new_balance': new_balance}
        else:
            cursor.close()
            connection.close()
            return {'error': 'Insufficient balance'}
    else:
        cursor.close()
        connection.close()
        return {'error': 'Invalid password'}

# Function for transferring cash from one user to another
def transfer_cash(from_password, to_username, amount):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM user WHERE password = %s', (from_password,))
    from_user = cursor.fetchone()
    cursor.execute('SELECT * FROM user WHERE username = %s', (to_username,))
    to_user = cursor.fetchone()

    if from_user and to_user:
        # Deduct the specified amount of cash from the sender's account
        new_from_balance = from_user[2] - int(amount)
        if new_from_balance >= 0:
            cursor.execute('UPDATE user SET Cash = %s WHERE password = %s', (new_from_balance, from_password))
            cursor.execute('UPDATE user SET Cash = Cash + %s WHERE username = %s', (amount, to_username))
            connection.commit()
            cursor.close()
            connection.close()
            return {'message': 'Cash transferred successfully', 'new_from_balance': new_from_balance}
        else:
            cursor.close()
            connection.close()
            return {'error': 'Insufficient balance'}
    else:
        cursor.close()
        connection.close()
        return {'error': 'Invalid password or username'}