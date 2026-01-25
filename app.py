from flask import Flask, render_template, request, redirect, session, url_for
from auth import register_user_db, login_user_db
from wallet import get_balance, update_balance
from slots import play_slots
from blackjack import play_blackjack
from history import show_bet_history

app = Flask(__name__)
app.secret_key = "casino_secret_key"

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        success = register_user_db(username, password)
        if success:
            return redirect(url_for("home"))
        else:
            return "User already exists"

    return render_template("register.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    user_id = login_user_db(username, password)
    if user_id:
        session["user_id"] = user_id
        return redirect(url_for("dashboard"))

    return "Invalid credentials"


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("home"))
    balance = get_balance(session["user_id"])
    return render_template("dashboard.html", balance=balance)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
