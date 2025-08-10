import json
from kafka import KafkaProducer
import random
from datetime import datetime

# Inicializa o KafkaProducer
producer = KafkaProducer(
    bootstrap_servers="localhost:9093",
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),  # Serializa para JSON
)

# Função para gerar dados de exemplo


def generate_message(i):
    return {
        "id": i,
        "timestamp": datetime.now().isoformat(),
        "user": f"user-{random.randint(1, 100)}",
        "event": f"event-{random.choice(['login', 'logout', 'purchase'])}",
        "amount": random.uniform(10.0, 1000.0) if random.random() > 0.5 else None,
        "metadata": {
            "location": f"location-{random.randint(1, 10)}",
            "device": random.choice(["mobile", "desktop", "tablet"]),
        },
    }


# Enviar mensagens para três tópicos
for i in range(6000):
    msg = generate_message(i)

    # Enviar para o primeiro tópico
    producer.send("my-topic", value=msg)
    print(f"> Enviado para my-topic: {msg}")

    # Enviar para o segundo tópico
    producer.send("my-topic-2", value=msg)
    print(f"> Enviado para my-topic-2: {msg}")

    # Enviar para o terceiro tópico
    producer.send("my-topic-3", value=msg)
    print(f"> Enviado para my-topic-3: {msg}")

# Garantir que todas as mensagens sejam enviadas
producer.flush()
producer.close()
