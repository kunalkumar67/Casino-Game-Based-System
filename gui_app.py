import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

from auth import register_user_db, login_user_db
from wallet import get_balance, update_balance
from slots_gui import play_slots_gui
from blackjack_gui import play_blackjack_gui
from roulette_gui import play_roulette_gui
from history import show_bet_history
from leaderboard import show_leaderboard_gui


# ----------- GLOBAL STATE -----------
current_user_id = None

# ----------- MAIN WINDOW -----------
root = tk.Tk()
root.title("Casino Game System")
root.geometry("750x550")
root.configure(bg="#0b1220")

# ----------- THEME COLORS -----------
BG = "#0b1220"
CARD = "#111827"
BTN_BLUE = "#2563eb"
BTN_GREEN = "#16a34a"
BTN_RED = "#dc2626"
TEXT = "white"

# ----------- HELPER FUNCTIONS -----------

def clear_screen():
    for widget in root.winfo_children():
        widget.destroy()

def header(title):
    tk.Label(
        root,
        text=title,
        font=("Arial", 22, "bold"),
        fg=TEXT,
        bg=BG
    ).pack(pady=15)

def button(text, command, color=BTN_BLUE):
    return tk.Button(
        root,
        text=text,
        command=command,
        width=22,
        font=("Arial", 11, "bold"),
        bg=color,
        fg="white",
        relief="flat",
        padx=5,
        pady=5
    )

# ----------- LOGIN SCREEN -----------

def go_to_login():
    clear_screen()
    header("🎰 CASINO LOGIN")

    frame = tk.Frame(root, bg=CARD, padx=30, pady=30)
    frame.pack(pady=20)

    tk.Label(frame, text="Username:", fg=TEXT, bg=CARD).pack()
    username_entry = tk.Entry(frame, width=30)
    username_entry.pack(pady=5)

    tk.Label(frame, text="Password:", fg=TEXT, bg=CARD).pack()
    password_entry = tk.Entry(frame, width=30, show="*")
    password_entry.pack(pady=5)

    def login_action():
        global current_user_id
        username = username_entry.get()
        password = password_entry.get()

        user_id = login_user_db(username, password)
        if user_id:
            current_user_id = user_id
            messagebox.showinfo("Success", "Login Successful!")
            go_to_dashboard()
        else:
            messagebox.showerror("Error", "Invalid Credentials")

    button("Login", login_action).pack(pady=10)
    button("Register", go_to_register, BTN_GREEN).pack(pady=5)

# ----------- REGISTER SCREEN -----------

def go_to_register():
    clear_screen()
    header("📝 REGISTER")

    frame = tk.Frame(root, bg=CARD, padx=30, pady=30)
    frame.pack(pady=20)

    tk.Label(frame, text="Username:", fg=TEXT, bg=CARD).pack()
    username_entry = tk.Entry(frame, width=30)
    username_entry.pack(pady=5)

    tk.Label(frame, text="Password:", fg=TEXT, bg=CARD).pack()
    password_entry = tk.Entry(frame, width=30, show="*")
    password_entry.pack(pady=5)

    def register_action():
        username = username_entry.get()
        password = password_entry.get()

        success = register_user_db(username, password)
        if success:
            messagebox.showinfo("Success", "Registration Successful!")
            go_to_login()
        else:
            messagebox.showerror("Error", "Username already exists")

    button("Register", register_action).pack(pady=10)
    button("Back to Login", go_to_login, BTN_RED).pack(pady=5)

# ----------- DASHBOARD -----------

def go_to_dashboard():
    clear_screen()

    balance = get_balance(current_user_id)

    header("🎮 CASINO DASHBOARD")

    bal_frame = tk.Frame(root, bg=CARD, padx=20, pady=10)
    bal_frame.pack(pady=10)

    tk.Label(
        bal_frame,
        text=f"💵 Balance: ₹{balance}",
        font=("Arial", 16, "bold"),
        fg="#16a34a",
        bg=CARD
    ).pack()

    button("Deposit Money", deposit_money).pack(pady=5)
    button("Play Slots 🎰", play_slots_gui_wrapper).pack(pady=5)
    button("Play Blackjack ♠️", lambda: play_blackjack_gui(current_user_id)).pack(pady=5)
    button("Play Roulette 🎡", lambda: play_roulette_gui(current_user_id)).pack(pady=5)
    button("View Bet History 📊", show_history_gui).pack(pady=5)
    button("View Leaderboard 🏆", lambda: show_leaderboard_gui(root)).pack(pady=5)
    button("Logout", go_to_login, BTN_RED).pack(pady=5)

# ----------- DEPOSIT -----------

def deposit_money():
    def submit_deposit():
        try:
            amount = float(amount_entry.get())
            if amount <= 0:
                messagebox.showerror("Error", "Amount must be positive")
                return
            update_balance(current_user_id, amount, "DEPOSIT")
            messagebox.showinfo("Success", f"₹{amount} deposited!")
            go_to_dashboard()
        except:
            messagebox.showerror("Error", "Invalid amount")

    clear_screen()
    header("💰 Deposit Money")

    amount_entry = tk.Entry(root, width=30)
    amount_entry.pack(pady=10)

    button("Submit", submit_deposit).pack(pady=10)
    button("Back", go_to_dashboard, BTN_RED).pack(pady=5)

# ----------- GAMES -----------

def play_slots_gui_wrapper():
    play_slots_gui(current_user_id)

def show_history_gui():
    show_bet_history(current_user_id)
    messagebox.showinfo("History", "Check terminal for bet history")
    go_to_dashboard()

# ----------- START APP -----------
go_to_login()
root.mainloop()
