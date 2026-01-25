import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import time
import pygame
pygame.mixer.init()

from wallet import get_balance, update_balance
from db import get_connection

root = None
user_id = None
table = None
dealer_frame = None
player_frame = None
score_label = None


# ----- CARD VALUES -----
CARD_VALUES = {
    "ace": 11, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6,
    "7": 7, "8": 8, "9": 9, "10": 10,
    "jack": 10, "queen": 10, "king": 10
}

def load_card_image(card_name):
    rank, suit = card_name.split("_of_")

    rank_map = {
        "ace": "A",
        "king": "K",
        "queen": "Q",
        "jack": "J",
        "10": "10",
        "9": "9",
        "8": "8",
        "7": "7",
        "6": "6",
        "5": "5",
        "4": "4",
        "3": "3",
        "2": "2"
    }

    suit_map = {
        "hearts": "H",
        "diamonds": "D",
        "clubs": "C",
        "spades": "S"
    }

    filename = f"{rank_map[rank]}{suit_map[suit]}"

    for ext in ["png", "jpg", "jpeg"]:
        path = os.path.join("cards", f"{filename}.{ext}")
        if os.path.exists(path):
            img = Image.open(path).resize((90, 130))
            return ImageTk.PhotoImage(img)

    # 🧯 SAFETY FALLBACK (won't crash your game)
    print(f"⚠ Missing card image for {card_name}")
    return None

def animated_deal(frame, card):
    img = load_card_image(card)
    if img is None:
        return

    lbl = tk.Label(frame, image=img, bg="#0b1220")
    lbl.image = img
    lbl.pack(side="left", padx=10)

    try:
        pygame.mixer.Sound("sounds/deal.wav").play()
    except:
        pass

    root.update()
    time.sleep(0.25)


def create_deck():
    ranks = ["ace","2","3","4","5","6","7","8","9","10","jack","queen","king"]
    suits = ["hearts","diamonds","clubs","spades"]
    deck = [f"{r}_of_{s}" for r in ranks for s in suits]
    random.shuffle(deck)
    return deck

def card_value(card):
    rank = card.split("_")[0]
    return CARD_VALUES[rank]

def calculate_score(hand):
    total = sum(card_value(c) for c in hand)
    aces = sum(1 for c in hand if c.startswith("ace"))
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total

def play_bg_music():
    try:
        pygame.mixer.music.load("sounds/bg.wav")
        pygame.mixer.music.play(-1)
    except:
        pass

def play_blackjack_gui(uid):
    global root, user_id, dealer_frame, player_frame, score_label

    user_id = uid
    root = tk.Toplevel()
    root.title("Blackjack ♠️")
    root.geometry("900x600")
    root.configure(bg="#0b1220")

    tk.Label(
        root, text="♠ BLACKJACK TABLE",
        font=("Arial", 20, "bold"),
        fg="white", bg="#0b1220"
    ).pack(pady=10)

    tk.Label(
        root, text=f"💵 Balance: ₹{get_balance(user_id)}",
        fg="#16a34a", bg="#0b1220",
        font=("Arial", 12)
    ).pack()

    tk.Label(root, text="Enter Bet:", fg="white", bg="#0b1220").pack(pady=5)
    bet_entry = tk.Entry(root)
    bet_entry.pack()

    table = tk.Frame(root, bg="#0b1220")
    table.pack(pady=20)

    tk.Label(table, text="Dealer Cards", fg="white", bg="#0b1220").pack()
    dealer_frame = tk.Frame(table, bg="#0b1220")
    dealer_frame.pack(pady=5)

    tk.Label(table, text="Your Cards", fg="white", bg="#0b1220").pack(pady=10)
    player_frame = tk.Frame(table, bg="#0b1220")
    player_frame.pack(pady=5)

    score_label = tk.Label(
        table, fg="green", bg="#0b1220",
        font=("Arial", 12)
    )
    score_label.pack(pady=5)

    def start_game():
        try:
            bet = float(bet_entry.get())
        except:
            messagebox.showerror("Error", "Invalid bet")
            return

        if bet <= 0 or bet > get_balance(user_id):
            messagebox.showerror("Error", "Insufficient balance")
            return

        deck = create_deck()
        player_hand = [deck.pop(), deck.pop()]
        dealer_hand = [deck.pop(), deck.pop()]

        update_table(player_hand, dealer_hand, deck, bet)

    tk.Button(
        root, text="Start Game",
        command=start_game,
        bg="#2563eb", fg="white"
    ).pack(pady=10)

def update_table(player_hand, dealer_hand, deck, bet):
    for w in dealer_frame.winfo_children():
        w.destroy()
    for w in player_frame.winfo_children():
        w.destroy()

    animated_deal(dealer_frame, dealer_hand[0])
    tk.Label(
        dealer_frame, text="🂠",
        font=("Arial", 40),
        fg="yellow", bg="#0b1220"
    ).pack(side="left", padx=10)

    for card in player_hand:
        animated_deal(player_frame, card)

    score_label.config(
        text=f"Your Score: {calculate_score(player_hand)}"
    )

    def hit():
        card = deck.pop()
        player_hand.append(card)
        animated_deal(player_frame, card)

        score = calculate_score(player_hand)
        score_label.config(text=f"Your Score: {score}")

        if score > 21:
            messagebox.showinfo("Result", "BUST!")
            update_balance(user_id, -bet, "BET")
            log_bet(bet, "LOSS")
            root.after(500, root.destroy)

    def stand():
        for w in dealer_frame.winfo_children():
            w.destroy()

        for card in dealer_hand:
            animated_deal(dealer_frame, card)

        while calculate_score(dealer_hand) < 17:
            dealer_hand.append(deck.pop())
            animated_deal(dealer_frame, dealer_hand[-1])

        dealer_score = calculate_score(dealer_hand)
        player_score = calculate_score(player_hand)

        if dealer_score > 21 or player_score > dealer_score:
            messagebox.showinfo("Result", "YOU WIN")
            update_balance(user_id, bet * 2, "WIN")
            result = "WIN"
        else:
            messagebox.showinfo("Result", "YOU LOSE")
            update_balance(user_id, -bet, "BET")
            result = "LOSS"

        log_bet(bet, result)
        root.after(500, root.destroy)

    btn_frame = tk.Frame(root, bg="#0b1220")
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="HIT", command=hit,
              bg="#16a34a", fg="white").pack(side="left", padx=20)
    tk.Button(btn_frame, text="STAND", command=stand,
              bg="#dc2626", fg="white").pack(side="right", padx=20)

def log_bet(bet, result):
    conn = get_connection()
    cursor = conn.cursor()
    BLACKJACK_GAME_ID = 2   # <-- change if needed

    cursor.execute(
    "INSERT INTO bets (user_id, game_id, bet_amount, result) VALUES (%s, %s, %s, %s)",
    (user_id, BLACKJACK_GAME_ID, bet, result)
)

    conn.commit()
    conn.close()
