#!/bin/bash

sh ./stop_services.sh
nohup sh stop_services.sh 

echo "[Iniciando serviços...]"

# Criar diretórios para logs e PIDs se não existirem
mkdir -p logs pids

# Inicia o Gateway
nohup python3 gateway.py > logs/gateway.log 2>&1 & 
echo $! > pids/gateway.pid
echo "[OK] Gateway iniciado"

# Inicia sensores

nohup python3 sensor_temperatura.py t1 escritorio1 > logs/sensor_t1.log 2>&1 & 
echo $! > pids/sensor_t1.pid
nohup python3 sensor_temperatura.py t2 escritorio2 > logs/sensor_t2.log 2>&1 & 
echo $! > pids/sensor_t2.pid
nohup python3 sensor_temperatura.py t3 escritorio3 > logs/sensor_t3.log 2>&1 & 
echo $! > pids/sensor_t3.pid

nohup python3 sensor_luminosidade.py s1 escritorio1 > logs/sensor_s1.log 2>&1 & 
echo $! > pids/sensor_s1.pid
nohup python3 sensor_luminosidade.py s2 escritorio2 > logs/sensor_s2.log 2>&1 & 
echo $! > pids/sensor_s2.pid
nohup python3 sensor_luminosidade.py s3 escritorio3 > logs/sensor_s3.log 2>&1 & 
echo $! > pids/sensor_s3.pid

nohup python3 sensor_fumaca.py f1 escritorio1 > logs/sensor_f1.log 2>&1 & 
echo $! > pids/sensor_f1.pid
nohup python3 sensor_fumaca.py f2 escritorio2 > logs/sensor_f2.log 2>&1 & 
echo $! > pids/sensor_f2.pid
nohup python3 sensor_fumaca.py f3 escritorio3 > logs/sensor_f3.log 2>&1 & 
echo $! > pids/sensor_f3.pid


# Inicia atuadores

nohup python3 atuador_ar_condicionado.py escritorio1 50051 > logs/atuador_001.log 2>&1 & 
echo $! > pids/atuador_001.pid
nohup python3 atuador_ar_condicionado.py escritorio2 50052 > logs/atuador_002.log 2>&1 & 
echo $! > pids/atuador_002.pid
nohup python3 atuador_ar_condicionado.py escritorio3 50053 > logs/atuador_003.log 2>&1 & 
echo $! > pids/atuador_003.pid
 
nohup python3 atuador_lampada.py escritorio1 50071 > logs/atuador_004.log 2>&1 & 
echo $! > pids/atuador_a004pid 
nohup python3 atuador_lampada.py escritorio1 50072 > logs/atuador_005.log 2>&1 & 
echo $! > pids/atuador_a005pid 
nohup python3 atuador_lampada.py escritorio2 50073 > logs/atuador_006.log 2>&1 & 
echo $! > pids/atuador_a006pid 
nohup python3 atuador_lampada.py escritorio2 50074 > logs/atuador_007.log 2>&1 & 
echo $! > pids/atuador_a007pid 
nohup python3 atuador_lampada.py escritorio3 50075 > logs/atuador_008.log 2>&1 & 
echo $! > pids/atuador_a008pid 

nohup python3 atuador_controle_incendio.py escritorio1 50061 > logs/atuador_009.log 2>&1 & 
echo $! > pids/atuador_a009pid 
nohup python3 atuador_controle_incendio.py escritorio2 50062 > logs/atuador_010.log 2>&1 & 
echo $! > pids/atuador_a010pid 
nohup python3 atuador_controle_incendio.py escritorio3 50063 > logs/atuador_011.log 2>&1 & 
echo $! > pids/atuador_a011pid 
 
echo "[Todos os serviços foram iniciados em segundo plano!]"
