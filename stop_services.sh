#!/bin/bash

echo "[Parando serviços...]"

if [ ! -d "pids" ]; then
    echo "[ERRO] Nenhum serviço está rodando ou os arquivos de PID não foram encontrados."
    exit 1
fi

# Mata os processos armazenados nos arquivos de PID
for pidfile in pids/*.pid; do
    if [ -f "$pidfile" ]; then
        pid=$(cat "$pidfile")
        kill "$pid" 2>/dev/null
        if [ $? -eq 0 ]; then
            echo "[OK] Serviço $(basename "$pidfile" .pid) parado"
        else
            echo "[ERRO] Falha ao parar $(basename "$pidfile" .pid)"
        fi
        rm -f "$pidfile"
    fi
done

echo "[Todos os serviços foram encerrados!]"
