## Dependências

`kafka-python`
`grpcio-tools`
`fastapi uvicorn`

## 📌 Rodar o  Kafka

### localmente:

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

navega pelo ternial até a pasta do projetro e rode:
```bash
docker compose -f docker-compose.yaml up
```

## 📌 Como Rodar o Sistema

### Via start_services.sh
```bash
sh start_services.sh
```
Isso irá rodar o gateway e alguns senssores e atuadores predefinidos.    

Parando:

```bash
sh stop_services.sh
```

### Manualmente

* Inicie os servidores gRPC/Atuadores (em diferentes terminais)
```bash
python atuador_lampada.py <sala> <porta> <endereco_ip> & 
python atuador_ar_condicionado.py <sala> <porta> <endereco_ip> & 
python atuador_controle_incendio.py <sala> <porta> <endereco_ip> & 
```
Exemplo: 
```bash
python atuador_lampada.py escritorio1 50071 127.0.0.1 & 
python atuador_ar_condicionado.py escritorio1 50051 127.0.0.1 & 
python atuador_controle_incendio.py escritorio1 50061 127.0.0.1 & 
```

* Rode o Gateway Inteligente

```bash
python gateway.py
```

* Rode os Sensores (em diferentes terminais)
```bash
python sensor_temperatura.py  <sensor_id> <sala> <kafka_server>
python sensor_luminosidade.py  <sensor_id> <sala> <kafka_server>
python sensor_fumaca.py  <sensor_id> <sala> <kafka_server>
```
Exemplo: 
```bash
python sensor_temperatura.py t1 escritorio1 &
python sensor_luminosidade.py s1 escritorio1 &
python sensor_fumaca.py f1 escritorio1 &
```

