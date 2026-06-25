import json 
import boto3
import time 
from datetime import datetime
from kafka import KafkaConsumer

# Minio client configuration 
s3 = boto3.client(
    's3',
    endpoint_url='http://localhost:9002',
    aws_access_key_id='admin',
    aws_secret_access_key='password123',
)

bucket_name = 'bronze-transactions'

#Define consumer configuration
consumer = KafkaConsumer(
    'stock-quotes',
    bootstrap_servers=['localhost:29092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='bronze-consumer',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("🚀 Consumer démarré... réception de données depuis Kafka et envoi vers Minio")

#Main Function
for message in consumer:
    record = message.value
    symbol = record.get('symbol','Unknown')
    fetched_at = record.get('fetched_at')
    ts = datetime.fromisoformat(fetched_at).strftime("%Y%m%dT%H%M%S")
    #ts = record.get('fetched_at', int(time.time()))
    #ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    key = f"{symbol}/{ts}.json"



    s3.put_object(
        Bucket=bucket_name, 
        Key=key, 
        Body=json.dumps(record),
        ContentType='application/json'
    )

    # message en francais 
    print(f"✅ Données pour le symbole {symbol} stockées dans Minio avec la clé {key}")