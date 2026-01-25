from db import get_connection

def get_balance(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT balance FROM users WHERE user_id = %s",
        (user_id,)
    )
    balance = cursor.fetchone()[0]

    conn.close()
    return balance


def update_balance(user_id, amount, txn_type):
    conn = get_connection()
    cursor = conn.cursor()

    # Update user balance
    cursor.execute(
        "UPDATE users SET balance = balance + %s WHERE user_id = %s",
        (amount, user_id)
    )

    # Log transaction
    cursor.execute(
        "INSERT INTO transactions (user_id, amount, txn_type) VALUES (%s, %s, %s)",
        (user_id, amount, txn_type)
    )

    conn.commit()
    conn.close()
