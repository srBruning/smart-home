# -*- coding: utf-8 -*-
import json
import time
import threading
from kafka import KafkaConsumer
import traceback
from atuadores_service import AtuadoresManager
from  descoberta_multicast import descoberta_multicast
from smart_service import aplicar_regras_sensor
from config import KAFKA_SERVER, TOPICOS_SENSORES, VERBOUSE
from sensores_service import SensoresManager
from api import iniciar_api  

atua_manager = AtuadoresManager()
sensores_manager = SensoresManager()

def consumir_sensores():
    """ Escuta os dados dos sensores no Kafka e aplica as regras de decisão. """
    consumer = KafkaConsumer(
        *TOPICOS_SENSORES,
        bootstrap_servers=KAFKA_SERVER,
        value_deserializer=lambda v: json.loads(v.decode('utf-8'))
    )

    print("[Gateway] Aguardando dados dos sensores...")

    for mensagem in consumer:
        sensor_data = mensagem.value
        sensor_id = sensor_data.get("sensor_id")
        sensor_tipo = sensor_data.get("sensor")
        valor = sensor_data.get("valor")
        timestamp = sensor_data.get("timestamp")
        sala = sensor_data.get("sala", "geral")
        
        if not sensor_id or not sensor_tipo or valor is None:
            print("[Gateway] Erro: Mensagem do sensor incompleta ou inválida.")
            continue

        # Atualiza os sensores na classe singleton
        sensores_manager.atualizar_sensor(sensor_id, sensor_tipo, valor, timestamp, sala)

        print(f"[Gateway] Sensor {sensor_id} ({sensor_tipo}): {valor}") if VERBOUSE else None

        # Aplica as regras de decisão
        aplicar_regras_sensor(sensor_tipo, valor, sala)

def atualizar_status_atuadores():
    """ Atualiza periodicamente o estado dos atuadores cadastrados. """
    while True:
        atua_manager.atualizar_status_atuadores()
        time.sleep(30)

def processar_msg_multicast( tipo, atuador_tipo, endereco, sala):
    try:
        # print(f"[Gateway] Mensagem multicast recebida. Tipo: {tipo}, enddereço: {endereco}.")
        # Registra os atuadores dinamicamente
        if tipo == "atuador":
            atua_manager.adicionar_atuador(atuador_tipo, endereco, sala)
            print(f"[Gateway] Atuador descoberto: {atuador_tipo} -> {endereco}") if VERBOUSE else None
        
        if tipo == "sensor":
            # Atualiza os sensores na classe singleton
            sensores_manager.atualizar_sensor(endereco, atuador_tipo, None, None)
    except:
        print("[Gateway] Erro ao decodificar mensagem UDP -> ", traceback.format_exc())

def iniciar_descoberta():
    """ Escuta mensagens multicast UDP para descobrir sensores e atuadores. """
    for tipo, atuador_tipo, endereco, sala in descoberta_multicast():
        # Inicia a thread para processar mensagens multicast
        multicast_process_thread = threading.Thread(target=processar_msg_multicast, args=( tipo, atuador_tipo, endereco, sala), daemon=True)
        multicast_process_thread.start()
def main():
    """ Inicializa o Gateway e inicia as threads. """

    # Inicia a descoberta de sensores e atuadores via multicast
    multicast_thread = threading.Thread(target=iniciar_descoberta, daemon=True)
    multicast_thread.start()
    
    # Inicia a thread para consumir sensores
    sensor_thread = threading.Thread(target=consumir_sensores, daemon=True)
    sensor_thread.start()

    # Inicia a atualização periódica dos atuadores
    status_thread = threading.Thread(target=atualizar_status_atuadores, daemon=True)
    status_thread.start()

    # Inicia a API REST em uma thread separada
    api_thread = threading.Thread(target=iniciar_api, daemon=True)
    api_thread.start()
    
    # Mantém o programa rodando
    sensor_thread.join()
    status_thread.join()
    multicast_thread.join()

if __name__ == "__main__":
    main()
