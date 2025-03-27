# -*- coding: utf-8 -*-
import socket
import json
from config import MULTICAST_GROUP, MULTICAST_PORT
from atuadores_service import AtuadoresManager

atua_manager = AtuadoresManager()

#  for tipo, atuador_tipo, endereco, sala in descoberta_multicast()
def descoberta_multicast():
    """ Escuta mensagens multicast UDP para descobrir sensores e atuadores. """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("", MULTICAST_PORT))

    grupo = socket.inet_aton(MULTICAST_GROUP)
    mreq = grupo + socket.inet_aton("0.0.0.0")
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    print(f"[Gateway] Aguardando dispositivos via multicast em {MULTICAST_GROUP}:{MULTICAST_PORT}...")

    while True:
        data, addr = sock.recvfrom(1024)
        try:
            mensagem = json.loads(data.decode("utf-8"))
            tipo = mensagem.get("tipo")
            atuador_tipo = mensagem.get("atuador_tipo")
            endereco = mensagem.get("endereco")
            sala = mensagem.get("sala")

            if not tipo or not atuador_tipo or not endereco:
                print("[Gateway] Mensagem multicast inválida recebida.")
                continue

            yield tipo, atuador_tipo, endereco, sala

        except json.JSONDecodeError:
            print("[Gateway] Erro ao decodificar mensagem UDP.")

def anunciar_atuador(tipo, endereco, sala):
    """ Envia uma mensagem multicast para anunciar um atuador. """
    mensagem = {
        "tipo": "atuador",
        "atuador_tipo": tipo,
        "endereco": endereco, 
        "sala": sala
    }
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

    sock.sendto(json.dumps(mensagem).encode("utf-8"), (MULTICAST_GROUP, MULTICAST_PORT))
    print(f"[Atuador] Anunciado: {tipo} -> {endereco}")
 