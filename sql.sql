-- Active: 1725886842956@@127.0.0.1@3306@db1
-- Create the 'accounts' table
CREATE TABLE accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    balance DECIMAL(10, 2) NOT NULL
);

-- Insert sample data into the 'accounts' table
INSERT INTO accounts (name, balance) VALUES ('Alice', 1000.00);
INSERT INTO accounts (name, balance) VALUES ('Bob', 1500.00);
INSERT INTO accounts (name, balance) VALUES ('Charlie', 2000.00);
