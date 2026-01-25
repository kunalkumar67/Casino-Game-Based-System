import random
from wallet import get_balance, update_balance
from db import get_connection

def play_slots(user_id):
    balance = get_balance(user_id)
    print(f"\n💰 Current Balance: ₹{balance}")

    bet = float(input("Enter bet amount: "))

    if bet <= 0:
        print("❌ Invalid bet amount")
        return

    if bet > balance:
        print("❌ Insufficient balance")
        return

    symbols = ["🍒", "🍋", "⭐", "7️⃣"]
    spin = [random.choice(symbols) for _ in range(3)]

    print("🎰 Spinning...")
    print(" | ".join(spin))

    if spin.count(spin[0]) == 3:
        win_amount = bet * 3
        print(f"🎉 YOU WIN ₹{win_amount}!")
        update_balance(user_id, win_amount, "WIN")

        result = "WIN"
    else:
        print("💔 You lost the bet.")
        update_balance(user_id, -bet, "BET")

        result = "LOSS"

    # Insert bet record
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO bets (user_id, game_id, bet_amount, result) VALUES (%s, %s, %s, %s)",
        (user_id, 1, bet, result)
    )

    conn.commit()
    conn.close()
