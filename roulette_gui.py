import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import time
import math
import pygame
import os

from wallet import get_balance, update_balance
from db import get_connection

pygame.mixer.init()

ROULETTE_NUMBERS = list(range(37))

def roulette_color(n):
    if n == 0:
        return "green"
    return "red" if n % 2 == 0 else "black"

# -----------------------------------------
def play_roulette_gui(user_id):
    win = tk.Toplevel()
    win.title("Roulette 🎡")
    win.geometry("700x650")
    win.configure(bg="#0b1220")

    balance = get_balance(user_id)

    tk.Label(win, text="🎡 ROULETTE TABLE", font=("Arial", 20, "bold"),
             fg="white", bg="#0b1220").pack(pady=10)

    bal_label = tk.Label(win, text=f"Balance: ₹{balance}",
                         fg="#16a34a", bg="#0b1220", font=("Arial", 12))
    bal_label.pack()

    # ---------------- BET UI ----------------
    tk.Label(win, text="Bet Amount", fg="white", bg="#0b1220").pack()
    bet_entry = tk.Entry(win)
    bet_entry.pack()

    bet_type = tk.StringVar(value="red")

    tk.Radiobutton(win, text="Red", variable=bet_type, value="red",
                   bg="#0b1220", fg="red").pack()
    tk.Radiobutton(win, text="Black", variable=bet_type, value="black",
                   bg="#0b1220", fg="white").pack()
    tk.Radiobutton(win, text="Number (0–36)", variable=bet_type, value="number",
                   bg="#0b1220", fg="yellow").pack()

    number_entry = tk.Entry(win)
    number_entry.pack(pady=5)

    # ---------------- CANVAS ----------------
    canvas = tk.Canvas(win, width=400, height=400, bg="#0b1220", highlightthickness=0)
    canvas.pack(pady=20)

    wheel_img = Image.open("roulette_assets/wheel.png").resize((350, 350))
    ball_img = Image.open("roulette_assets/ball.png").resize((18, 18))

    wheel_angle = 0
    ball_angle = 0

    wheel_tk = ImageTk.PhotoImage(wheel_img)
    ball_tk = ImageTk.PhotoImage(ball_img)

    wheel_id = canvas.create_image(200, 200, image=wheel_tk)
    ball_id = canvas.create_image(200, 50, image=ball_tk)

    result_label = tk.Label(win, text="", font=("Arial", 14),
                            fg="white", bg="#0b1220")
    result_label.pack(pady=10)

    # ---------------- SPIN LOGIC ----------------
    def spin():
        nonlocal wheel_angle, ball_angle, wheel_tk, ball_tk

        try:
            bet = float(bet_entry.get())
        except:
            messagebox.showerror("Error", "Invalid bet")
            return

        if bet <= 0 or bet > get_balance(user_id):
            messagebox.showerror("Error", "Insufficient balance")
            return

        try:
            pygame.mixer.Sound("roulette_assets/rspin.wav").play()
        except:
            pass

        speed = 25
        for i in range(60):
            wheel_angle -= speed
            ball_angle += speed * 1.5
            speed *= 0.97  # deceleration

            rotated = wheel_img.rotate(wheel_angle)
            wheel_tk = ImageTk.PhotoImage(rotated)
            canvas.itemconfig(wheel_id, image=wheel_tk)

            x = 200 + 140 * math.cos(math.radians(ball_angle))
            y = 200 + 140 * math.sin(math.radians(ball_angle))
            canvas.coords(ball_id, x, y)

            win.update()
            time.sleep(0.03)

        result = random.choice(ROULETTE_NUMBERS)
        color = roulette_color(result)

        result_label.config(
            text=f"🎯 Result: {result} ({color.upper()})",
            fg=color if color != "green" else "lightgreen"
        )

        win_flag = False
        payout = 0
        choice = bet_type.get()

        if choice == "red" and color == "red":
            win_flag = True
            payout = bet * 2
        elif choice == "black" and color == "black":
            win_flag = True
            payout = bet * 2
        elif choice == "number":
            try:
                if int(number_entry.get()) == result:
                    win_flag = True
                    payout = bet * 36
            except:
                pass

        if win_flag:
            update_balance(user_id, payout, "WIN")
            log_bet(user_id, bet, "WIN")
            pygame.mixer.Sound("roulette_assets/rwin.wav").play()
            messagebox.showinfo("WIN", f"You won ₹{payout}!")
        else:
            update_balance(user_id, -bet, "LOSS")
            log_bet(user_id, bet, "LOSS")
            pygame.mixer.Sound("roulette_assets/rlose.wav").play()
            messagebox.showinfo("LOSE", "You lost!")

        bal_label.config(text=f"Balance: ₹{get_balance(user_id)}")

    tk.Button(win, text="SPIN 🎡", command=spin,
              bg="#2563eb", fg="white", font=("Arial", 13)).pack(pady=15)

# ---------------- DATABASE ----------------
def log_bet(user_id, bet, result):
    conn = get_connection()
    cursor = conn.cursor()
    ROULETTE_GAME_ID = 3
    cursor.execute(
        "INSERT INTO bets (user_id, game_id, bet_amount, result) VALUES (%s,%s,%s,%s)",
        (user_id, ROULETTE_GAME_ID, bet, result)
    )
    conn.commit()
    conn.close()
