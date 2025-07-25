from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers="localhost:9093",
    value_serializer=lambda v: v.encode("utf-8"),  # transforma string em bytes
)

# Enviar 5 mensagens
for i in range(9999):
    msg = f"Mensagem Kafka #{i}"
    producer.send("my-topic", value=msg)
    print(f"> Enviado: {msg}")

producer.flush()
producer.close()
