import json
import time
import random
from datetime import datetime, timezone
from kafka import KafkaProducer

# =========================
# CONFIGURATION KAFKA
# =========================
producer = KafkaProducer(
    bootstrap_servers=["localhost:29092"],
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

# =========================
# LISTE DES ACTIONS
# =========================
symbols = ["AAPL", "TSLA", "GOOGL", "AMZN", "MSFT", "NVDA"]

print("🚀 Producer démarré... envoi de données vers Kafka")

# =========================
# LOOP INFINIE
# =========================
while True:
    symbol = random.choice(symbols)

    # simulation prix réaliste
    price = round(random.uniform(100, 1000), 2)
    volume = random.randint(100, 5000)

    message = {
        "symbol": symbol,
        "price": price,
        "volume": volume,
        "fetched_at": int(time.time())
    }

    producer.send("stock-quotes", value=message)

    print(f"📤 Envoyé: {message}")

    # pause pour simuler flux temps réel
    time.sleep(2)