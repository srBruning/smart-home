## Dependências

```bash
pip install kafka-python
pip install grpcio-tools
pip install fastapi uvicorn
```


## 📌 Rodar o  Kafka

### localmente:
https://huzzefakhan.medium.com/install-and-setup-apache-kafka-on-linux-b430d8796dae
https://mmarcosab.medium.com/usando-apache-kafka-e-apache-zookeeper-no-windows-3e48e76e795f


vai denpender de como instalou, se for linux e baixou, entrra na pasta do kafka e executa:   
O zookeeper:
```bash
bin/zookeeper-server-start.sh config/zookeeper.properties 
```
E o Kafka:
```bash
bin/kafka-server-start.sh config/server.properties
```

### Via Doker-compose

https://medium.com/@ygorppolvere/kafka-com-docker-dedbbe9eff76

nvaega pelo ternial até a pasta do projetro e rode:
```bash
docker compose -f docker-compose.yaml up
```

## 📌 Como Rodar o Sistema
* Inicie os servidores gRPC/Atuadores (em diferentes terminais)
```bash
python atuador_ar_condicionado.py
python atuador_lampada.py
python atuador_controle_incendio.py
```

*Obs*: não implementei a descobreta Muklticast *ainda*, a conexão com os atuadores está fixa, por isso é importante todar todos eles primeiro.   

* Rode o Gateway Inteligente

```bash
python gateway.py
```

* Rode os Sensores (em diferentes terminais)
```bash
python sensor_temperatura.py
python sensor_luminosidade.py
python sensor_fumaca.py

```

