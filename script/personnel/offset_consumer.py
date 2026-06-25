from kafka import KafkaConsumer, TopicPartition

BOOTSTRAP_SERVERS = ['localhost:29092']
GROUP_ID = 'bronze-consumer'
TOPIC = 'stock-quotes'

consumer = KafkaConsumer(
    bootstrap_servers=BOOTSTRAP_SERVERS,
    group_id=GROUP_ID
)

partitions = consumer.partitions_for_topic(TOPIC)

if not partitions:
    print(f"❌ Topic '{TOPIC}' introuvable")
    exit()

print(f"\n📌 Offsets du groupe '{GROUP_ID}'\n")

for partition in partitions:
    tp = TopicPartition(TOPIC, partition)

    committed = consumer.committed(tp)

    if committed is None:
        print(f"Partition {partition}: Aucun offset enregistré")
    else:
        print(f"Partition {partition}: offset={committed}")

consumer.close()