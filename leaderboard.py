import tkinter as tk
from db import get_connection

def show_leaderboard_gui(root):
    win = tk.Toplevel(root)
    win.title("Leaderboard 🏆")
    win.geometry("500x400")
    win.configure(bg="#0b1220")

    tk.Label(win, text="🏆 TOP PLAYERS 🏆", font=("Arial", 18, "bold"), fg="white", bg="#0b1220").pack(pady=10)

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT username, balance
    FROM users
    ORDER BY balance DESC
    LIMIT 10;
    """

    cursor.execute(query)
    players = cursor.fetchall()
    conn.close()

    frame = tk.Frame(win, bg="#111827", padx=20, pady=20)
    frame.pack(pady=10)

    tk.Label(frame, text="Rank  |  Username  |  Balance", fg="white", bg="#111827").pack()
    tk.Label(frame, text="------------------------------------", fg="white", bg="#111827").pack()

    rank = 1
    for username, balance in players:
        tk.Label(frame, text=f"{rank}.  {username:<10}  ₹{balance}", fg="#16a34a", bg="#111827").pack()
        rank += 1

    tk.Button(win, text="Close", command=win.destroy, bg="#2563eb", fg="white").pack(pady=10)
