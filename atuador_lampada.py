# -*- coding: utf-8 -*-

import threading
import grpc
from concurrent import futures
import sys
from config import TIPO_LAMPADA, VERBOUSE
import atuadores_pb2
import atuadores_pb2_grpc
from descoberta_multicast import anunciar_atuador
import time
 

estado_lampada = False
rodandando = True

class LampadaServicer(atuadores_pb2_grpc.LampadaServicer):
    def LigarLampada(self, request, context):
        global estado_lampada
        estado_lampada = True
        print("Ligar lampada") if VERBOUSE else None
        return atuadores_pb2.RespostaAtuador(mensagem="+Lâmpada ligada.")

    def DesligarLampada(self, request, context):
        global estado_lampada
        estado_lampada = False
        print("Desligar lampada") if VERBOUSE else None
        return atuadores_pb2.RespostaAtuador(mensagem="-Lâmpada desligada.")

    def GetEstadoLampada(self, request, context):
        print("responsendo o estado da lampada: ",   "ligada" if estado_lampada else "desligado") if VERBOUSE else None
        return atuadores_pb2.EstadoAtuador(ligado=estado_lampada)

def serve(porta):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    atuadores_pb2_grpc.add_LampadaServicer_to_server(LampadaServicer(), server)
    server.add_insecure_port(f'[::]:{porta}')
    server.start()
    print(f"Servidor Lâmpada rodando na porta {porta}...")


    server.wait_for_termination()

def anunciar(endereco, porta, sala):
    global rodandando
    while rodandando:
        anunciar_atuador(TIPO_LAMPADA, f"{endereco}:{porta}", sala)
        time.sleep(30)

if __name__ == "__main__":

    sala = sys.argv[1] if len(sys.argv) > 1 else "geral"
    porta = sys.argv[2] if len(sys.argv) > 2 else "50051"
    endereco = sys.argv[3] if len(sys.argv) > 3 else "127.0.0.1"
   
    print(f"Endereço: {endereco}, Porta: {porta}, Sala: {sala}")
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
