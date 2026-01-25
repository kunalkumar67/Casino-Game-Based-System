from auth import register_user_db, login_user_db
from wallet import get_balance, update_balance
from slots import play_slots
from blackjack import play_blackjack
from history import show_bet_history

def user_menu(user_id):
    while True:
        print("\n🎮 USER MENU 🎮")
        print("1. View Balance")
        print("2. Deposit Money")
        print("3. Play Slots 🎰")
        print("4. Play Blackjack ♠️")
        print("5. View Bet History 📊")
        print("6. Logout")

        choice = input("Choose option: ")

        if choice == "1":
            balance = get_balance(user_id)
            print(f"💵 Balance: ₹{balance}")

        elif choice == "2":
            amount = float(input("Enter deposit amount: "))
            update_balance(user_id, amount, "DEPOSIT")
            print("✅ Money deposited")

        elif choice == "3":
            play_slots(user_id)

        elif choice == "4":
            play_blackjack(user_id)

        elif choice == "5":
            show_bet_history(user_id)

        elif choice == "6":
            break

        else:
            print("Invalid option")

def main():
    while True:
        print("\n🎰 CASINO GAME SYSTEM 🎰")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Choose option: ")

        if choice == "1":
            username = input("Enter username: ")
            password = input("Enter password: ")
            register_user_db(username, password)
            print("✅ Registration successful!")

        elif choice == "2":
            username = input("Enter username: ")
            password = input("Enter password: ")
            user_id = login_user_db(username, password)

            if user_id:
                print(f"✅ Login successful! User ID: {user_id}")
                user_menu(user_id)   # <-- THIS WAS MISSING
            else:
                print("❌ Login failed! Wrong username or password.")

        elif choice == "3":
            print("Bye 👋")
            break

        else:
            print("Invalid option")

if __name__ == "__main__":
    main()

