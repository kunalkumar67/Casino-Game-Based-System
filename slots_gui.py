import random
import tkinter as tk
from tkinter import messagebox
from wallet import get_balance, update_balance
from db import get_connection
import pygame
import time
pygame.mixer.init()


def play_slots_gui(user_id):
    win = tk.Toplevel()
    win.title("Slots 🎰")
    win.geometry("450x350")

    balance = get_balance(user_id)

    tk.Label(win, text="🎰 SLOT MACHINE", font=("Arial", 16, "bold")).pack(pady=10)
    bal_label = tk.Label(win, text=f"Balance: ₹{balance}", fg="green")
    bal_label.pack()

    tk.Label(win, text="Enter Bet Amount:").pack(pady=5)
    bet_entry = tk.Entry(win)
    bet_entry.pack()

    symbols = ["🍒", "🍋", "⭐", "7️⃣"]

    # -------- SLOT DISPLAY (THIS WAS MISSING) --------
    slot_frame = tk.Frame(win)
    slot_frame.pack(pady=10)

    slot1 = tk.StringVar(value="❓")
    slot2 = tk.StringVar(value="❓")
    slot3 = tk.StringVar(value="❓")

    tk.Label(slot_frame, textvariable=slot1, font=("Arial", 24)).pack(side="left", padx=10)
    tk.Label(slot_frame, textvariable=slot2, font=("Arial", 24)).pack(side="left", padx=10)
    tk.Label(slot_frame, textvariable=slot3, font=("Arial", 24)).pack(side="left", padx=10)
    # -----------------------------------------------

    result_label = tk.Label(win, text="", font=("Arial", 14))
    result_label.pack(pady=10)

    def spin():
        try:
            bet = float(bet_entry.get())
        except:
            messagebox.showerror("Error", "Enter a valid number")
            return

        if bet <= 0:
            messagebox.showerror("Error", "Bet must be greater than 0")
            return

        if bet > get_balance(user_id):
            messagebox.showerror("Error", "Insufficient balance")
            return

        # Play spinning sound
        try:
            pygame.mixer.Sound("sounds/spins.wav").play()
        except:
            pass  # if sound missing, just continue

        # ANIMATION: spin for ~1.5 seconds
        for _ in range(15):
            slot1.set(random.choice(symbols))
            slot2.set(random.choice(symbols))
            slot3.set(random.choice(symbols))
            win.update()
            time.sleep(0.08)

        # Final result
        s1 = random.choice(symbols)
        s2 = random.choice(symbols)
        s3 = random.choice(symbols)

        slot1.set(s1)
        slot2.set(s2)
        slot3.set(s3)

        conn = get_connection()
        cursor = conn.cursor()

        if s1 == s2 == s3:
            win_amount = bet * 5
            update_balance(user_id, win_amount, "WIN")

            try:
                pygame.mixer.Sound("sounds/win.wav").play()
            except:
                pass

            result_label.config(text=f"🎉 YOU WIN ₹{win_amount}!", fg="green")
            result = "WIN"
        else:
            update_balance(user_id, -bet, "BET")

            try:
                pygame.mixer.Sound("sounds/lose.wav").play()
            except:
                pass

            result_label.config(text="😞 You lost", fg="red")
            result = "LOSS"

        # Log bet in DB
        def log_bet(bet, result):
            conn = get_connection()
            cursor = conn.cursor()

            SLOT_GAME_ID = 1   # must match games table

            cursor.execute(
                "INSERT INTO bets (user_id, game_id, bet_amount, result) VALUES (%s, %s, %s, %s)",
                (user_id, SLOT_GAME_ID, bet, result)
    )
        conn.commit()
        conn.close()

        # Update balance label
        bal_label.config(text=f"Balance: ₹{get_balance(user_id)}")

    tk.Button(win, text="SPIN 🎰", command=spin, bg="gold").pack(pady=10)
