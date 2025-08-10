import json
from kafka import KafkaProducer

# Inicializa o KafkaProducer
producer = KafkaProducer(
    bootstrap_servers="localhost:9093",
    value_serializer=lambda v: json.dumps(
        v).encode("utf-8"),  # Serializa para JSON
)

# Ler o arquivo JSON com os filmes do Ghibli
with open("ghibli-movies.json", "r", encoding="utf-8") as file:
    films_data = json.load(file)

for i in range(1000):  # Loop externo
    # Enviar cada filme um por vez para o tópico "ghibli-movies"
    for film in films_data["films"]:
        producer.send("ghibli-movies", value=film)
        print(f"> Enviado para ghibli-movies: {film['name']}")

# Garantir que todas as mensagens sejam enviadas
producer.flush()
producer.close()
