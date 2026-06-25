import json
import time
import requests
from datetime import datetime, timezone
from kafka import KafkaProducer

API_KEY = "d8t9p99r01qhcnk0tl20d8t9p99r01qhcnk0tl2g"
BASE_URL = "https://finnhub.io/api/v1/quote"

print("🚀 Producer démarré... envoi de données vers Kafka")

# =========================
# LISTE DES ACTIONS
# =========================
symbols = ["AAPL", "TSLA", "GOOGL", "AMZN", "MSFT", "NVDA"]

producer = KafkaProducer(
    bootstrap_servers=["localhost:29092"],
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def fetch_quote(symbol):
    url = f"{BASE_URL}?symbol={symbol}&token={API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        data['symbol'] = symbol
        data['fetched_at'] = datetime.now(timezone.utc).isoformat()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la récupération des données pour {symbol}: {e}")
        return None

while True:
    for symbol in symbols:
        quote_data = fetch_quote(symbol)
        if quote_data:
            producer.send("stock-quotes", value=quote_data)
            print(f"✅ Données envoyées pour {symbol}: {quote_data}")
        else:
            print(f"⚠️ Aucune donnée envoyée pour {symbol} en raison d'une erreur.")
    time.sleep(5)  # Attendre 5 secondes avant la prochaine itération


