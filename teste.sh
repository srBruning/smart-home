sudo echo "teste"

python3 gateway.py & 


echo "Ar condicionado"
python3 atuador_ar_condicionado.py escritorio1 50051 &
python3 atuador_ar_condicionado.py escritorio2 50052 &
python3 atuador_ar_condicionado.py escritorio3 50053 &
sleep 1
echo "Lampadas"
python3 atuador_lampada.py escritorio1 50071 127.0.0.1 & 
python3 atuador_lampada.py escritorio1 50072 127.0.0.1 & 
python3 atuador_lampada.py escritorio2 50073 127.0.0.1 & 
python3 atuador_lampada.py escritorio2 50074 127.0.0.1 & 
python3 atuador_lampada.py escritorio3 50075 127.0.0.1 & 

echo "Controle de incendio"
python3 atuador_controle_incendio.py escritorio1 50061 & 
python3 atuador_controle_incendio.py escritorio2 50062 & 
python3 atuador_controle_incendio.py escritorio3 50063 & 

echo "Sensores"
python3 sensor_temperatura.py t1 escritorio1 127.0.0.1:9092 &
python3 sensor_temperatura.py t2 escritorio2 127.0.0.1:9092 &
python3 sensor_temperatura.py t3 escritorio3 127.0.0.1:9092 &

python3 sensor_luminosidade.py s1 escritorio1 127.0.0.1:9092 &
python3 sensor_luminosidade.py s2 escritorio2 127.0.0.1:9092 &
python3 sensor_luminosidade.py s3 escritorio3 127.0.0.1:9092 &

python3 sensor_fumaca.py f1 escritorio1 127.0.0.1:9092 &
python3 sensor_fumaca.py f2 escritorio2 127.0.0.1:9092 &
python3 sensor_fumaca.py f3 escritorio3 127.0.0.1:9092 &
 
sleep 2
echo "-------------------"
curl -X POST "http://127.0.0.1:8000/api/atuadores/ligar" -H "Content-Type: application/json" -d '{"tipo": "ar-condicionado", "endereco": "127.0.0.1:50052"}'
echo "-------------------"

# npx http-server frontend -C-1  

sleep 200

sudo killall -9 python3
