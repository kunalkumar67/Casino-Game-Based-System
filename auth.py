import hashlib
from db import get_connection

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user_db(username, password):
    password_hash = hash_password(password)

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
            (username, password_hash)
        )
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def login_user_db(username, password):
    password_hash = hash_password(password)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT user_id FROM users WHERE username=%s AND password_hash=%s",
        (username, password_hash)
    )

    user = cursor.fetchone()
    conn.close()

    return user[0] if user else None
