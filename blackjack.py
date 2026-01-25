import random
from wallet import get_balance, update_balance
from db import get_connection

def draw_card():
    cards = [2,3,4,5,6,7,8,9,10,10,10,11]  # 11 = Ace
    return random.choice(cards)

def calculate_score(hand):
    # If Ace causes bust, treat it as 1 instead of 11
    if sum(hand) > 21 and 11 in hand:
        hand[hand.index(11)] = 1
    return sum(hand)

def play_blackjack(user_id):
    balance = get_balance(user_id)
    print(f"\n💰 Current Balance: ₹{balance}")

    bet = float(input("Enter bet amount: "))

    if bet <= 0:
        print("❌ Invalid bet amount")
        return

    if bet > balance:
        print("❌ Insufficient balance")
        return

    # Initial hands
    player_hand = [draw_card(), draw_card()]
    dealer_hand = [draw_card(), draw_card()]

    print(f"\nYour cards: {player_hand} → Score: {calculate_score(player_hand)}")
    print(f"Dealer shows: [{dealer_hand[0]}, ?]")

    # Player turn
    while True:
        choice = input("\nType 'h' to hit or 's' to stand: ").lower()

        if choice == "h":
            player_hand.append(draw_card())
            print(f"Your cards: {player_hand} → Score: {calculate_score(player_hand)}")

            if calculate_score(player_hand) > 21:
                print("💥 BUST! You lose.")
                update_balance(user_id, -bet, "BET")
                result = "LOSS"
                break

        elif choice == "s":
            break
        else:
            print("Invalid input! Type 'h' or 's'.")

    player_score = calculate_score(player_hand)

    # Dealer turn (only if player not busted)
    if player_score <= 21:
        print(f"\nDealer cards: {dealer_hand} → Score: {calculate_score(dealer_hand)}")

        while calculate_score(dealer_hand) < 17:
            dealer_hand.append(draw_card())
            print(f"Dealer draws... New score: {calculate_score(dealer_hand)}")

        dealer_score = calculate_score(dealer_hand)

        # Decide winner
        if dealer_score > 21:
            print("🎉 Dealer busted! You WIN!")
            update_balance(user_id, bet * 2, "WIN")
            result = "WIN"

        elif player_score > dealer_score:
            print("🎉 You WIN!")
            update_balance(user_id, bet * 2, "WIN")
            result = "WIN"

        elif player_score == dealer_score:
            print("🤝 It's a TIE! Bet returned.")
            # No wallet change
            result = "TIE"

        else:
            print("💔 You LOSE.")
            update_balance(user_id, -bet, "BET")
            result = "LOSS"

    # Log bet in database
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO bets (user_id, game_id, bet_amount, result) VALUES (%s, %s, %s, %s)",
        (user_id, 2, bet, result)
    )

    conn.commit()
    conn.close()
