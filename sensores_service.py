# -*- coding: utf-8 -*-


class SensoresManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.dados_sensores = {}  # Armazena os dados dos sensores
        return cls._instance

    def atualizar_sensor(self, sensor_id, sensor_tipo, valor, timestamp, sala="geral"):

        if valor is None and sensor_id in self.dados_sensores:
            estado_atual = self.dados_sensores[sensor_id]
            valor = estado_atual.get("valor")
            timestamp = estado_atual.get("timestamp") 

        """ Atualiza ou adiciona um sensor ao dicionário. """
        self.dados_sensores[sensor_id] = {
            "sensor_id": sensor_id,
            "tipo": sensor_tipo,
            "valor": valor,
            "timestamp": timestamp,
            "sala": sala
        }

    def obter_sensor(self, sensor_id):
        """ Retorna os dados do sensor pelo ID. """
        return self.dados_sensores.get(sensor_id, None)

    def listar_sensores(self):
        """ Retorna todos os sensores registrados. """
        return list(self.dados_sensores.values())

    def remover_sensor(self, sensor_id):
        """ Remove um sensor pelo ID. """
        if sensor_id in self.dados_sensores:
            del self.dados_sensores[sensor_id]
