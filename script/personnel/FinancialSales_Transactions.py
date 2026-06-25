import random
import time
import simplejson as json
#import datetime as datetime
from faker import Faker
from confluent_kafka import SerializingProducer
from confluent_kafka.serialization import StringSerializer
from confluent_kafka import Consumer
from datetime import datetime, timezone

fake = Faker("fr_FR")

def generate_sales_transaction():
    user = fake.simple_profile()
    return {
        "transaction_id": fake.uuid4(),
        "product_id": random.choice(["Product1", "Product2", "Product3","Product4","Product5","Product6","Product7"]),
        "product_name": random.choice(["Ordinateur", "Smartphone", "Tablette","Imprimante","Casque","Enceinte","Cable"]),
        "product_category": random.choice(["Electronique", "Informatique", "Téléphonie","Son","Accessoire"]),
        "product_price": round(random.uniform(10, 1000), 2),
        "product_quantity": random.randint(1, 10),
        "product_brand": random.choice(['apple', 'samsung', 'oneplus', 'mi', 'boat', 'sony']),
        "currency": random.choice(['USD', 'GBP']),
        "customer_id": user['username'],
        # FORMAT DE DATE CORRIGÉ pour correspondre à Jackson
        "transaction_date": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
        "payment_method": random.choice(['credit_card', 'debit_card', 'online_transfer'])
    }

def delivery_report(err, msg):
    if err is not None:
        print(f"Échec de la livraison du message: {err}")
    else:
        print(f"Message Livré à {msg.topic()} [{msg.partition()}]")

def Main():
    topic = "FinancialSales_Transactions"
    producer = SerializingProducer({
        "bootstrap.servers": "localhost:29092",
        #"value.serializer": StringSerializer("utf_8"),
        #"key.serializer": StringSerializer("utf_8")
    })

    current_time = datetime.now()

    while (datetime.now() - current_time).seconds < 120:

        try:
            transaction = generate_sales_transaction()
            transaction['totalAmount'] = transaction['product_price'] * transaction['product_quantity']
        
            print(transaction)

            producer.produce(topic=topic, 
                             key=transaction["transaction_id"], 
                             value=json.dumps(transaction), 
                             on_delivery=delivery_report
                             )

            producer.poll(0)
            time.sleep(5)

        except BufferError:
            print(f"Tampon plein! patientez...")
            time.sleep(1)
        except Exception as e:
            print(f"Erreur: {e}")

    # Fermer proprement le producer
    producer.flush()

if __name__ == "__main__":
    Main()