# -*- coding: utf-8 -*-
import threading
import grpc
from concurrent import futures
import atuadores_pb2 as atuadores_pb2
import atuadores_pb2_grpc as atuadores_pb2_grpc
import sys
from descoberta_multicast import anunciar_atuador
from config import TIPO_AR_CONDICIONADO, VERBOUSE
import time

estado_ar_condicionado = False
temperatura_atual = 24.0  # Temperatura inicial
rodandando = True

class ArCondicionadoServicer(atuadores_pb2_grpc.ArCondicionadoServicer):
    def LigarArCondicionado(self, request, context):
        print("Ligando ar-condicionado") if VERBOUSE else None
        global estado_ar_condicionado
        estado_ar_condicionado = True
        print("Ligando ar-condicionado") if VERBOUSE else None 
        return atuadores_pb2.RespostaAtuador(mensagem="Ar-Condicionado ligado.")

    def DesligarArCondicionado(self, request, context):
        print("Desligando ar-condicionado") if VERBOUSE else None 
        global estado_ar_condicionado
        estado_ar_condicionado = False
        print("Deligando ar condicionado") if VERBOUSE else None 
        return atuadores_pb2.RespostaAtuador(mensagem="Ar-Condicionado desligado.")

    def SetTemperatura(self, request, context):
        print(f"[SetTemperatura] nova temperatura: {request.temperatura}°C") if VERBOUSE else None 
        global temperatura_atual
        temperatura_atual = request.temperatura
        mensagem=f"Temperatura ajustada para {temperatura_atual}°C."
        print(mensagem) if VERBOUSE else None 
        return atuadores_pb2.RespostaAtuador(mensagem=mensagem)

    def GetTemperatura(self, request, context):
        print(f"[GetTemperatura] estado: ligado= {estado_ar_condicionado}, temperatura= {temperatura_atual}") if VERBOUSE else None 
        return atuadores_pb2.EstadoTemperaturaAtuador(
            ligado=estado_ar_condicionado, 
            temperatura=temperatura_atual
        )
    
def serve(porta):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    atuadores_pb2_grpc.add_ArCondicionadoServicer_to_server(ArCondicionadoServicer(), server)
    server.add_insecure_port(f'[::]:{porta}')
    server.start()
    print(f"Servidor ar-condicionado rodando na porta {porta}...")

    server.wait_for_termination()

def anunciar(endereco, porta, sala):
    global rodandando
    while rodandando:
        anunciar_atuador(TIPO_AR_CONDICIONADO, f"{endereco}:{porta}", sala)
        time.sleep(15)

if __name__ == "__main__":
    sala = sys.argv[1] if len(sys.argv) > 1 else "geral"
    porta = sys.argv[2] if len(sys.argv) > 2 else "50051"
    endereco = sys.argv[3] if len(sys.argv) > 3 else "127.0.0.1"

    server_thread = threading.Thread(target=serve, args=(porta,), daemon=True)
    server_thread.start()

    # Aguarda um tempo para o servidor subir
    time.sleep(1)
    rodandando = True
    multicast_thread = threading.Thread(target=anunciar, args=(endereco, porta, sala), daemon=True)
    multicast_thread.start()

    server_thread.join()
    print("Encerando servidor...")
    rodandando = False
    multicast_thread.terminate()
    print("Servidor finalizado.")