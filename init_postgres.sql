CREATE TABLE IF NOT EXISTS user_logins (
    id SERIAL PRIMARY KEY,
    username TEXT,
    event_type TEXT,
    event_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sent_to_kafka BOOLEAN DEFAULT FALSE
);