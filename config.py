# -*- coding: utf-8 -*-
import yaml

# Caminho do arquivo de configuração
CONFIG_FILE = "config.yaml"

def carregar_config():
    """ Carrega as configurações do arquivo YAML. """
    with open(CONFIG_FILE, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)

# Carrega a configuração na inicialização
config = carregar_config()

# Definições globais de configuração
VERBOUSE = config["geral"]["verbose"]
MULTICAST_GROUP = config["multicast"]["group"]
MULTICAST_PORT = config["multicast"]["port"]

KAFKA_SERVER = config["kafka"]["server"]
TOPICOS_SENSORES = config["kafka"]["topics"]

TEMPERATURA_PADRAO = config["atuadores"]["temperatura_padrao"]


TIPO_AR_CONDICIONADO = "ar-condicionado"
TIPO_LAMPADA = "lampada"
TIPO_CONTROLE_INCENDIO = "controle-incendio"