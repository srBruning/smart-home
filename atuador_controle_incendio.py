# -*- coding: utf-8 -*-
import threading
import time
import grpc
from concurrent import futures
import atuadores_pb2 as atuadores_pb2
import atuadores_pb2_grpc as atuadores_pb2_grpc
import sys
from config import TIPO_CONTROLE_INCENDIO, VERBOUSE
from descoberta_multicast import anunciar_atuador

estado_controle_incendio = False
rodandando = True

class ControleIncendioServicer(atuadores_pb2_grpc.ControleIncendioServicer):
    def AtivarControleIncendio(self, request, context):
        global estado_controle_incendio
        estado_controle_incendio = True
        print("AtivarControleIncendio") if VERBOUSE else None
        return atuadores_pb2.RespostaAtuador(mensagem="Sistema de Controle de Incêndio ativado.")

    def DesativarControleIncendio(self, request, context):
        global estado_controle_incendio
        estado_controle_incendio = False
        print("DesativarControleIncendio") if VERBOUSE else None
        return atuadores_pb2.RespostaAtuador(mensagem="Sistema de Controle de Incêndio desativado.")

    def GetEstadoControleIncendio(self, request, context):
        print("[GetEstadoControleIncendio] estado: ligado= ",estado_controle_incendio ) if VERBOUSE else None
        return atuadores_pb2.EstadoAtuador(ligado=estado_controle_incendio)

def serve(porta):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    atuadores_pb2_grpc.add_ControleIncendioServicer_to_server(ControleIncendioServicer(), server)
    server.add_insecure_port(f'[::]:{porta}')
    server.start()
    print(f"Servidor Controle de Incêndio rodando na porta {porta}...")

    server.wait_for_termination()

def anunciar(endereco, porta, sala):
    global rodandando
    while rodandando:
        anunciar_atuador(TIPO_CONTROLE_INCENDIO, f"{endereco}:{porta}", sala)
        time.sleep(30)

if __name__ == "__main__":
    sala = sys.argv[1] if len(sys.argv) > 1 else "geral"
    porta = sys.argv[2] if len(sys.argv) > 2 else "50051"
    endereco = sys.argv[3] if len(sys.argv) > 3 else "127.0.0.1"

    server_thread = threading.Thread(target=serve, args=(porta,), daemon=True)
    server_thread.start()

    # Aguarda um tempo para o servidor subir
    time.sleep(1)
    rodandando = True
    multicast_thread = threading.Thread(target=anunciar, args=(endereco, porta, sala,), daemon=True)
    multicast_thread.start()

    server_thread.join()
    print("Encerando servidor...")
    rodandando = False
    multicast_thread.terminate()
    print("Servidor finalizado.")