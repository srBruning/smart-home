# -*- coding: utf-8 -*-
import sys
import json
import time
import random
from kafka import KafkaProducer
from config import KAFKA_SERVER, VERBOUSE

# Obtém os parâmetros passados na inicialização
if len(sys.argv) < 3:
    print("Uso: python sensor_fumaca.py <sensor_id> <sala> <kafka_server>")
    sys.exit(1)
kafka_server = KAFKA_SERVER

sensor_id = sys.argv[1]
sala = sys.argv[2] if len(sys.argv) > 2 else "geral"
if len(sys.argv) > 3:
    kafka_server = sys.argv[3]

producer = KafkaProducer(
    bootstrap_servers=kafka_server,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def gerar_dados():
    return {
        "sensor_id": sensor_id,
        "sensor": "fumaca",
        "valor": round(random.uniform(0, 1), 2),
        "timestamp": time.time(),
        "sala": sala
    }

if __name__ == "__main__":
    while True:
        dados = gerar_dados()
        print(f"[Sensor {sensor_id}] Enviando: {dados}") if VERBOUSE else None
        producer.send("sensor-fumaca", value=dados)
        time.sleep(5)
