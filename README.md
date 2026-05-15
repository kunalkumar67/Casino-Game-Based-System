# 🎰 Casino Game Based System

> A full-featured casino game system with Slots, Blackjack & Roulette. GUI-based (Tkinter) with MySQL database, authentication, and bet tracking.

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![MySQL](https://img.shields.io/badge/mysql-8.0%2B-orange)](https://www.mysql.com/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## 📋 Table of Contents

- [Features](#features)
- [Project Overview](#project-overview)
- [Installation](#installation)
- [Usage](#usage)
- [GUI Screenshots](#gui-screenshots)
  - [Authentication](#authentication)
  - [Casino Dashboard](#casino-dashboard)
  - [Games](#games)
  - [Game History & Leaderboard](#game-history--leaderboard)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Database Schema](#database-schema)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

- 🎰 **Multiple Casino Games**: Slots, Blackjack, and Roulette with realistic mechanics
- 🔐 **User Authentication**: Secure sign-up and login system with password hashing
- 💾 **Database Integration**: MySQL 8.0 for wallet management and bet tracking
- 🎨 **Modern GUI**: Built with Tkinter for smooth and intuitive user experience
- 🎵 **Animations & Sound**: Realistic game animations and audio effects
- 📊 **Game History**: Track all bets and view comprehensive leaderboards
- ⚡ **Multiple Interfaces**: Terminal, Flask web server, and GUI support for flexibility
- 💰 **Wallet Management**: Real-time balance updates and bet tracking

## 📖 Project Overview

### Application Server (app.py)
<img width="900" height="350" alt="app.py server" src="https://github.com/user-attachments/assets/22e6f0c9-c024-42fa-b23d-0318cbb4b1a2" />

### Application Interface (app.py)
<img width="900" height="350" alt="app.py interface" src="https://github.com/user-attachments/assets/755c6054-b9c9-41aa-b471-0e1f3e4347c9" />

### Terminal Interface (main.py)
<img width="900" height="650" alt="main.py server" src="https://github.com/user-attachments/assets/0fe4002e-1df6-4137-88f7-fde1cd3ef183" />

## 🔧 Installation

### Prerequisites

- **Python** 3.8 or higher
- **MySQL** 8.0 or higher
- **pip** (Python package manager)

### Step-by-Step Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/kunalkumar67/Casino-Game-Based-System.git
   cd Casino-Game-Based-System
   ```

2. **Install Python Dependencies**
   ```bash
   pip install flask mysql-connector-python pygame tkinter
   ```

3. **Setup MySQL Database**
   ```sql
   CREATE DATABASE casino_db;
   ```
   - Update MySQL credentials in `db.py`:
     - Host
     - Username
     - Password
     - Database name

4. **Run the Application**
   ```bash
   # Flask web version
   python app.py
   
   # Tkinter GUI version
   python gui_app.py
   
   # Terminal version
   python main.py
   ```

## 🎮 Usage

### Starting the GUI Application
```bash
python gui_app.py
```

### Game Instructions

1. **Sign Up / Log In**: Create an account or log in with existing credentials
2. **Choose a Game**: Select from Slots, Blackjack, or Roulette
3. **Place Your Bet**: Enter your bet amount
4. **Play**: Follow game-specific instructions (spin, hit, etc.)
5. **View History**: Check your betting history and leaderboard rankings

## 🖼️ GUI Screenshots

### Authentication

#### Sign-Up / Sign-In Page
<img width="1700" height="900" alt="Sign-Up/Sign-In Page" src="https://github.com/user-attachments/assets/bd238ee2-f1be-4be8-aadd-a7e879ad8cf2" />

#### Login Page
<img width="1700" height="900" alt="Login Page" src="https://github.com/user-attachments/assets/e7194ace-e0ba-4362-8494-b2af5d90969f" />

### Casino Dashboard

#### Main Dashboard
<img width="1700" height="900" alt="Casino Dashboard" src="https://github.com/user-attachments/assets/a0fc5e09-d033-41b8-a194-66205f462795" />

### Games

#### 🎰 Slots Game

**Enter Bet Amount & Play**
<img width="1700" height="900" alt="Slots - Enter Bet" src="https://github.com/user-attachments/assets/1f092a47-4fd2-460c-9b9b-fccfe13c3a62" />

**Spin & Results**
<img width="1700" height="900" alt="Slots - Spin/Win Lose" src="https://github.com/user-attachments/assets/21878952-cb2a-4f16-b055-c59e2c2c1763" />

#### 🃏 Blackjack Game

**Enter Bet & Start Game**
<img width="1700" height="900" alt="Blackjack - Enter Bet & Start" src="https://github.com/user-attachments/assets/18db8036-aa60-4920-8be1-fe6ee683ca53" />

**Win/Loss Results**
<img width="1700" height="900" alt="Blackjack - Win/Loss" src="https://github.com/user-attachments/assets/a24d2030-5d8c-4586-92f8-57c5f5883737" />

#### 🎡 Roulette Game

**Enter Bet & Spin**
<img width="1700" height="900" alt="Roulette - Enter Bet & Spin" src="https://github.com/user-attachments/assets/2944ffea-fef4-4483-8191-bdfdcbd3b164" />

**Win/Loss & Logout**
<img width="1700" height="900" alt="Roulette - Win/Loss & Logout" src="https://github.com/user-attachments/assets/0d9284ef-95fd-4dc3-baa1-54bb07c7d137" />

### Game History & Leaderboard

#### Leaderboard
<img width="1700" height="900" alt="Leaderboard" src="https://github.com/user-attachments/assets/f1e63439-2a73-4361-8b01-46f96c777c03" />

#### Bet History - GUI Dashboard
<img width="1700" height="900" alt="Bet History - Dashboard" src="https://github.com/user-attachments/assets/1c20b753-ea3f-4ef3-bfdb-fe0d8b58052c" />

#### Bet History - Terminal View
<img width="1700" height="900" alt="Bet History - Terminal" src="https://github.com/user-attachments/assets/1831f014-87a1-41e1-86fb-109283580dac" />

## 📁 Project Structure

```
Casino-Game-Based-System/
├── app.py                    # Flask web application
├── gui_app.py               # Main GUI application entry point
├── main.py                  # Terminal-based version
├── auth.py                  # Authentication logic
├── db.py                    # Database connection
├── wallet.py                # Wallet management
├── history.py               # Bet history tracking
├── leaderboard.py           # Leaderboard management
├── slots.py                 # Slots game logic
├── slots_gui.py             # Slots GUI implementation
├── blackjack.py             # Blackjack game logic
├── blackjack_gui.py         # Blackjack GUI implementation
├── roulette_gui.py          # Roulette GUI implementation
├── card_renamer_gui.py      # Card asset utility
├── cards/                   # Card image assets
├── sounds/                  # Audio effects
├── roulette_assets/         # Roulette wheel assets
├── Templates/               # Flask HTML templates
├── Tables/                  # Database schema files
└── README.md               # This file
```

## 🛠️ Technologies Used

| Technology | Purpose | Version |
|-----------|---------|---------|
| **Python** | Core language | 3.8+ |
| **Tkinter** | GUI framework | Built-in |
| **Flask** | Web framework | Latest |
| **MySQL** | Database | 8.0+ |
| **Pygame** | Game assets & sounds | Latest |
| **mysql-connector** | Database connector | Latest |

## 💾 Database Schema

The system uses MySQL with the following key tables:

- **users**: User accounts with authentication
- **wallets**: User wallet balances
- **bets**: Betting history and results
- **leaderboard**: User rankings and statistics

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Created by**: [kunalkumar67](https://github.com/kunalkumar67)

**Language Composition**: 
- Python: 91%
- HTML: 9%

⭐ If you find this project helpful, please consider giving it a star!
