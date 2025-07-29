from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers="localhost:9093",
    value_serializer=lambda v: v.encode("utf-8"),  # transforma string em bytes
)

# Enviar n mensagens
for i in range(9999):
    msg = f"Mensagem Kafka #{i}"
    producer.send("my-topic", value=msg)
    print(f"> Enviado: {msg} topic 1")

# Enviar n mensagens
for i in range(9999):
    msg = f"Mensagem Kafka #{i}"
    producer.send("my-topic-2", value=msg)
    print(f"> Enviado: {msg} topic 2")

# Enviar n mensagens
for i in range(9999):
    msg = f"Mensagem Kafka #{i}"
    producer.send("my-topic-3", value=msg)
    print(f"> Enviado: {msg} topic 3")

producer.flush()
producer.close()
