# producer.py

import psycopg2
import json
from kafka import KafkaProducer
import time

# Подключение к PostgreSQL
def connect_postgres():
    return psycopg2.connect(
        dbname="test_db",
        user="admin",
        password="admin",
        host="localhost",
        port=5432
    )

# Подключение к Kafka
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def send_events():
    conn = connect_postgres()
    cursor = conn.cursor()

    # Получаем непереданные события
    cursor.execute("""
        SELECT id, username, event_type, extract(epoch from event_time)
        FROM user_logins
        WHERE sent_to_kafka = FALSE
        LIMIT 100
        FOR UPDATE SKIP LOCKED
    """)
    rows = cursor.fetchall()

    for row in rows:
        data = {
            "id": row[0],
            "user": row[1],
            "event": row[2],
            "timestamp": row[3]
        }
        producer.send("user_events", value=data)
        print(f"Sent to Kafka: {data}")

    # Обновляем флаг отправки
    if rows:
        cursor.execute("""
            UPDATE user_logins
            SET sent_to_kafka = TRUE
            WHERE id IN (SELECT id FROM user_logins WHERE sent_to_kafka = FALSE LIMIT 100)
        """)
        conn.commit()

    conn.close()

if __name__ == "__main__":
    while True:
        send_events()
        time.sleep(5)