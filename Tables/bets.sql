CREATE TABLE bets (
    bet_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    game_id INT,
    bet_amount DECIMAL(10,2),
    result ENUM('WIN','LOSS'),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
