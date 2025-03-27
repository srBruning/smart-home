# -*- coding: utf-8 -*-
import grpc
import atuadores_pb2
import atuadores_pb2_grpc

from config import TIPO_AR_CONDICIONADO, TIPO_LAMPADA, TIPO_CONTROLE_INCENDIO, TEMPERATURA_PADRAO, VERBOUSE


class AtuadoresManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.dados_atuadores = {}
            cls._instance.clientes = {
                TIPO_AR_CONDICIONADO: [],
                TIPO_LAMPADA: [],
                TIPO_CONTROLE_INCENDIO: []
            }
        return cls._instance

    def atuadores(self, tipo=None):
        """Gera os atuadores cadastrados de um tipo específico ou todos."""
        if tipo:
            yield from self.clientes.get(tipo, [])
        else:
            for tipo, lista in self.clientes.items():
                yield from lista
    

    def criar_stub(self, tipo, endereco):
        """Cria um stub gRPC baseado no tipo do atuador."""
        if tipo == TIPO_AR_CONDICIONADO:
            return atuadores_pb2_grpc.ArCondicionadoStub(grpc.insecure_channel(endereco))
        elif tipo == TIPO_LAMPADA:
            return atuadores_pb2_grpc.LampadaStub(grpc.insecure_channel(endereco))
        elif tipo == TIPO_CONTROLE_INCENDIO:
            return atuadores_pb2_grpc.ControleIncendioStub(grpc.insecure_channel(endereco))
        return None

    def adicionar_atuador(self, tipo, endereco, sala="geral"):
        """Adiciona um novo atuador dinamicamente."""
        
        if tipo not in self.clientes:
            print(f"[Gateway] Tipo de atuador inválido: {tipo}")
            return

        if any(obj["endereco"] == endereco for obj in self.clientes[tipo]):
            print(f"[Gateway] Atuador {tipo} em {endereco} já está cadastrado.") if VERBOUSE else None
            return

        print(f"*** [Gateway] Adicionando atuador {tipo} em {endereco}") if VERBOUSE else None
        stub = self.criar_stub(tipo, endereco)
        if stub:
            self.clientes[tipo].append({
                "endereco": endereco,
                "tipo": tipo,
                "stub": stub,
                "sala": sala,
                "ligado": None,
                "adicional": TEMPERATURA_PADRAO if tipo == TIPO_AR_CONDICIONADO else None,
                "auto_mode": True  # Ativado por padrão
            })
            print(f"[Gateway] Atuador {tipo} em {endereco} adicionado!!") if VERBOUSE else None
            print("--- Atualizando atuadores ----") if VERBOUSE else None
            self.atualizar_status_atuadores()            
        
        print(self.clientes) if VERBOUSE else None

    def find_stub(self, tipo, endereco):
        """Busca o stub gRPC pelo tipo e endereço do atuador."""
        for obj in self.atuadores(tipo):
            if obj["endereco"] == endereco:
                return obj["stub"]
        print(f"[Gateway] {tipo.capitalize()} em {endereco} não encontrado.")
        return None

    def validar_atuador(self, tipo, endereco):
        """Busca o stub gRPC pelo tipo e endereço do atuador."""
        for obj in self.atuadores(tipo):
            if obj["endereco"] == endereco:
                return True
        print(f"[Gateway] {tipo.capitalize()} em {endereco} não encontrado.")
        return False

    # Métodos específicos para cada atuador
    def ligar_ar_condicionado(self, endereco):
        if (stub := self.find_stub(TIPO_AR_CONDICIONADO, endereco)):
            resposta = stub.LigarArCondicionado(atuadores_pb2.ComandoVazio())
            print(f"[Gateway] Resposta: {resposta.mensagem}") if VERBOUSE else None

    def desligar_ar_condicionado(self, endereco):
        if (stub := self.find_stub(TIPO_AR_CONDICIONADO, endereco)):
            resposta = stub.DesligarArCondicionado(atuadores_pb2.ComandoVazio())
            print(f"[Gateway] {resposta.mensagem}") if VERBOUSE else None

    def set_temperatura_ar_condicionado(self, endereco, temperatura):
        if (stub := self.find_stub(TIPO_AR_CONDICIONADO, endereco)):
            resposta = stub.SetTemperatura(atuadores_pb2.TemperaturaAtuador(temperatura=temperatura))
            print(f"[Gateway] {resposta.mensagem}") #if VERBOUSE else None

    def get_temperatura_ar_condicionado(self, endereco):
        if (stub := self.find_stub(TIPO_AR_CONDICIONADO, endereco)):
            resposta = stub.GetTemperatura(atuadores_pb2.ComandoVazio())
            estado = "ligado" if resposta.ligado else "desligado"
            print(f"[Gateway] Ar-Condicionado está {estado}, Temperatura: {resposta.temperatura}°C") if VERBOUSE else None
            return resposta.ligado, resposta.temperatura
        return None, None

    def ligar_lampada(self, endereco):
        if (stub := self.find_stub(TIPO_LAMPADA, endereco)):
            resposta = stub.LigarLampada(atuadores_pb2.ComandoVazio())
            print(f"[Gateway] {resposta.mensagem}") if VERBOUSE else None

    def desligar_lampada(self, endereco):
        if (stub := self.find_stub(TIPO_LAMPADA, endereco)):
            resposta = stub.DesligarLampada(atuadores_pb2.ComandoVazio())
            print(f"[Gateway] {resposta.mensagem}") if VERBOUSE else None

    def get_estado_lampada(self, endereco):
        print(f"[Gateway] Buscando estado da lampada em {endereco}") if VERBOUSE else None
        if (stub := self.find_stub(TIPO_LAMPADA, endereco)):
            resposta = stub.GetEstadoLampada(atuadores_pb2.ComandoVazio())
            return resposta.ligado
        return None

    def ativar_controle_incendio(self, endereco):
        if (stub := self.find_stub(TIPO_CONTROLE_INCENDIO, endereco)):
            resposta = stub.AtivarControleIncendio(atuadores_pb2.ComandoVazio())
            print(f"[Gateway] {resposta.mensagem}") if VERBOUSE else None

    def desativar_controle_incendio(self, endereco):
        if (stub := self.find_stub(TIPO_CONTROLE_INCENDIO, endereco)):
            resposta = stub.DesativarControleIncendio(atuadores_pb2.ComandoVazio())
            print(f"[Gateway] {resposta.mensagem}") if VERBOUSE else None

    def get_estado_controle_incendio(self, endereco):
        if (stub := self.find_stub(TIPO_CONTROLE_INCENDIO, endereco)):
            resposta = stub.GetEstadoControleIncendio(atuadores_pb2.ComandoVazio())
            return resposta.ligado
        return None

    def atualizar_status_atuadores(self):
        """Atualiza o estado de todos os atuadores conhecidos."""
        for tipo, lista in self.clientes.items():
            for obj in lista:
                endereco = obj["endereco"]
                if tipo == TIPO_AR_CONDICIONADO:
                    obj["ligado"], obj["adicional"] = self.get_temperatura_ar_condicionado(endereco)
                elif tipo == TIPO_LAMPADA:
                    obj["ligado"] = self.get_estado_lampada(endereco)
                elif tipo == TIPO_CONTROLE_INCENDIO:
                    obj["ligado"] = self.get_estado_controle_incendio(endereco)

    def definir_modo_atuador(self, endereco, modo_automatico: bool):
        """ Define se um atuador pode ser alterado automaticamente. """
        for tipo, lista in self.clientes.items():
            for atuador in lista:
                if atuador["endereco"] == endereco:
                    atuador["auto_mode"] = modo_automatico
                    estado = "Automático" if modo_automatico else "Manual"
                    print(f"[Gateway] Atuador {atuador['tipo']} em {endereco} agora está no modo {estado}.") if VERBOUSE else None
                    return True
        print(f"[Gateway] Atuador em {endereco} não encontrado.")
        return False

    def pode_alterar_atuador(self, endereco):
        """ Verifica se um atuador pode ser alterado automaticamente. """
        for tipo, lista in self.clientes.items():
            for atuador in lista:
                if atuador["endereco"] == endereco:
                    return atuador["auto_mode"] 
        return False