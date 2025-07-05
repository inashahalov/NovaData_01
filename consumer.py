from kafka import KafkaConsumer
import json
from clickhouse_driver import Client
from datetime import datetime, timezone  # ✅ Импорт добавлен

consumer = KafkaConsumer(
    'user_events',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='user-logins-consumer',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

clickhouse_client = Client(
    host='localhost',
    port=9000,
    user='user',
    password='strongpassword'
)

print("Consumer started...")

for message in consumer:
    print("Received:", message.value)
    data = message.value

    try:
        dt = datetime.fromtimestamp(data['timestamp'], tz=timezone.utc)  # ✅ Теперь работает

        clickhouse_client.execute(
            "INSERT INTO test.user_events (id, user, event, event_time) VALUES",
            [(data['id'], data['user'], data['event'], dt)]
        )
        print("Saved to ClickHouse")
    except Exception as e:
        print("Error saving to ClickHouse:", e)