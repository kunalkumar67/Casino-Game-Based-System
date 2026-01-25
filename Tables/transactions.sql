CREATE TABLE transactions (
    txn_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    amount DECIMAL(10,2),
    txn_type ENUM('BET','WIN','DEPOSIT'),
    txn_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
