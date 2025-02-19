import mysql.connector
from mysql.connector import Error

def get_users_with_expiry():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="admin_user",
            password="admin_password",
            database="python_expiry_test"
        )
        if conn.is_connected():
            print("Connected to the database")
            cursor = conn.cursor(dictionary=True)
            query = """
            SELECT FullName, Email, ExpiryDate 
            FROM Contracts
            WHERE ExpiryDate <= CURDATE() + INTERVAL 5 DAY 
            AND EmailSent = FALSE
            """
            cursor.execute(query)
            users = cursor.fetchall()
            cursor.close()
            conn.close()
            return users
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def update_email_sent_status(email):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="admin_user",
            password="admin_password",
            database="python_expiry_test"
        )
        if conn.is_connected():
            print("Emails read.")
            cursor = conn.cursor()
            query = "UPDATE Contracts SET EmailSent = TRUE WHERE Email = %s"
            cursor.execute(query, (email,))
            conn.commit()
            cursor.close()
            conn.close()
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None