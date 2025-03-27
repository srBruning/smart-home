# -*- coding: utf-8 -*-


import datetime
import time
from atuadores_service import AtuadoresManager
from config import TIPO_AR_CONDICIONADO, TIPO_LAMPADA, TIPO_CONTROLE_INCENDIO, VERBOUSE, TEMPERATURA_PADRAO

atua_manager = AtuadoresManager()


class DecisoesManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.pilha_decisoes = []
        return cls._instance

    def adicionar_decisao(self,endereco, sala, msg):
        self.pilha_decisoes.insert(0, f"[{sala} - {endereco}]: {msg} [{time.strftime('%H:%M:%S')}]")
        if len(self.pilha_decisoes) > 20:
            self.pilha_decisoes.pop( len(self.pilha_decisoes) - 1 )
    
    def get_decisoes(self):
        return list(self.pilha_decisoes)

dmanager = DecisoesManager()

# 🔹 Métodos para processar cada tipo de sensor
def processar_sensor_temperatura(valor, sala):
    print(f"[Gateway] Temperatura recebida: {valor}°C sala: {sala}") #if VERBOUSE else None

    for obj in atua_manager.atuadores(TIPO_AR_CONDICIONADO):
        stub = obj.get("stub")
        endereco = obj.get("endereco")

        # Verifica se o atuador está na mesma sala
        if obj["sala"] != sala:
            continue

        # Verifica se o atuador está em modo automático
        if not atua_manager.pode_alterar_atuador(endereco):
            print(f"[Gateway] Ignorando ajuste automático para {endereco} (modo manual).")
            continue
        
        # temperatura_padrao = float(obj.get("adicional", 20.0))

        if not stub or not endereco:
            print("[Gateway] Erro: Atuador de ar-condicionado sem stub ou endereço válido.")
            continue

        ar_ligado, temperatura_atual = atua_manager.get_temperatura_ar_condicionado(endereco)

        # Se o ar-condicionado estiver desligado e a temperatura estiver 4°C acima ou abaixo da padrão
        if not ar_ligado and (valor > TEMPERATURA_PADRAO + 4 or valor < TEMPERATURA_PADRAO - 4):
            print(f"[Gateway] Ligando ar-condicionado e ajustando para {TEMPERATURA_PADRAO}°C") if VERBOUSE else None
            dmanager.adicionar_decisao(endereco, sala, f"Ligando ar-condicionado e ajustando para {TEMPERATURA_PADRAO}°C")
            atua_manager.ligar_ar_condicionado(endereco)
            atua_manager.set_temperatura_ar_condicionado(endereco, TEMPERATURA_PADRAO)

        # Se o ar-condicionado já estiver ligado, ajustar apenas se necessário
        elif ar_ligado and temperatura_atual != TEMPERATURA_PADRAO:
            print(f"[Gateway] Ajustando temperatura para {TEMPERATURA_PADRAO}°C") #if VERBOUSE else None
            dmanager.adicionar_decisao(endereco, sala, f"Ajustando temperatura para {TEMPERATURA_PADRAO}°C")
            atua_manager.set_temperatura_ar_condicionado(endereco, TEMPERATURA_PADRAO)

def processar_sensor_luminosidade(valor, sala):
    print(f"[Gateway] Luminosidade recebida: {valor}%") if VERBOUSE else None

    for atuador in atua_manager.atuadores(TIPO_LAMPADA):

        # Verifica se o atuador está na mesma sala
        if atuador.get("sala") != sala:
            continue
        stub = atuador.get("stub")
        endereco = atuador.get("endereco")

        # Verifica se o atuador está em modo automático
        if not atua_manager.pode_alterar_atuador(endereco):
            print(f"[Gateway] Ignorando ajuste automático para {endereco} (modo manual).") if VERBOUSE else None
            continue

        if not stub or not endereco:
            print("[Gateway] Erro: Atuador de lâmpada sem stub ou endereço válido.")
            continue

        if valor < 30:
            dmanager.adicionar_decisao(endereco, sala, f"ligar lampada")
            atua_manager.ligar_lampada(endereco)
        elif valor > 70:
            dmanager.adicionar_decisao(endereco, sala, f"deligar lampada")
            atua_manager.desligar_lampada(endereco)

def processar_sensor_fumaca(valor, sala):
    print(f"[Gateway] Fumaça detectada: {valor}") if VERBOUSE else None

    for atuador in atua_manager.atuadores(TIPO_CONTROLE_INCENDIO):
        stub = atuador.get("stub")
        endereco = atuador.get("endereco")

        # Verifica se o atuador está na mesma sala
        if atuador.get("sala") != sala:
            continue

        if not stub or not endereco:
            print("[Gateway] Erro: Atuador de controle de incêndio sem stub ou endereço válido.")
            continue

        if valor > 0.6:
            dmanager.adicionar_decisao(endereco, sala, f"ativar controle de incendio")
            atua_manager.ativar_controle_incendio(endereco)
        elif valor < 0.4:
            dmanager.adicionar_decisao(endereco, sala, f"desativar controle de incendio")
            atua_manager.desativar_controle_incendio(endereco)

def aplicar_regras_sensor(sensor_tipo, valor, sala):
    if sensor_tipo == "temperatura":
        processar_sensor_temperatura(valor, sala)
    elif sensor_tipo == "luminosidade":
        processar_sensor_luminosidade(valor, sala)
    elif sensor_tipo == "fumaca":
        processar_sensor_fumaca(valor, sala)
