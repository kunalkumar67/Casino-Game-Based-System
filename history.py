from db import get_connection

def show_bet_history(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT 
        b.bet_id,
        g.game_name,
        b.bet_amount,
        b.result,
        b.created_at
    FROM bets b
    JOIN games g ON b.game_id = g.game_id
    WHERE b.user_id = %s
    ORDER BY b.created_at DESC;
    """

    cursor.execute(query, (user_id,))
    records = cursor.fetchall()

    conn.close()

    print("\n📊 YOUR BET HISTORY 📊")
    print("-" * 70)

    if not records:
        print("No bets found.")
        return

    print(f"{'Bet ID':<8} | {'Game':<12} | {'Amount':<10} | {'Result':<6} | {'Time'}")
    print("-" * 70)

    for bet_id, game_name, amount, result, time in records:
        print(f"{bet_id:<8} | {game_name:<12} | ₹{amount:<9} | {result:<6} | {time}")

    print("-" * 70)
