from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel
from atuadores_service import AtuadoresManager
from config import TIPO_AR_CONDICIONADO, TIPO_CONTROLE_INCENDIO, TIPO_LAMPADA
from sensores_service import SensoresManager
import threading
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from smart_service import DecisoesManager

# Instâncias dos gerenciadores
atua_manager = AtuadoresManager()
sensores_manager = SensoresManager()

dmanager = DecisoesManager()
app = FastAPI(docs_url="/")

# Habilita CORS para permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite qualquer origem (pode restringir se quiser)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AtuadorComando(BaseModel):
    """ Modelo para receber comandos de controle de atuadores via API REST. """
    tipo: str
    endereco: str

class SetTemperaturaComando(BaseModel):
    """ Modelo para mudar a temperatura do ar-condicionado. """
    endereco: str
    temperatura: float

class ModoAtuadorComando(BaseModel):
    """ Modelo para alterar o modo de operação do atuador. """
    endereco: str
    auto_mode: bool

# # Monta a pasta "frontend" como arquivos estáticos
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

@app.get("/app")
def root():
    return FileResponse("frontend/index.html")

# Outros endpoints da API...
#     
@app.get("/api")
def root():
    return {"mensagem": "API REST do Gateway Inteligente está rodando!"}

@app.get("/api/sensores")
def listar_sensores():
    """ Retorna todos os sensores registrados. """
    return sensores_manager.listar_sensores()

class ModoAtuadorComando(BaseModel):
    """ Modelo para alterar o modo de operação do atuador. """
    endereco: str
    auto_mode: bool
    
@app.get("/api/atuadores")
def listar_atuadores():
    """ Retorna todos os atuadores registrados. """
    atuadores = []
    
    for atuador in atua_manager.atuadores():
        atuadores.append({
            "tipo": atuador["tipo"],
            "endereco": atuador["endereco"],
            "ligado": atuador["ligado"],
            "sala": atuador.get("sala"),
            "adicional": atuador.get("adicional"),
            "auto_mode": atuador.get("auto_mode")

        })
    return atuadores

@app.post("/api/atuadores/ligar")
def ligar_atuador(comando: AtuadorComando):
    """ Liga um atuador específico pelo tipo e endereço. """

    tipo = comando.tipo
    endereco = comando.endereco
    print("[API] /atuadores/ligar ", tipo, endereco)

    stub = atua_manager.find_stub(tipo, endereco)
    if not stub:
        raise HTTPException(status_code=404, detail="Atuador não encontrado.")


    if tipo not in [TIPO_AR_CONDICIONADO, TIPO_LAMPADA, TIPO_CONTROLE_INCENDIO]:
        raise HTTPException(status_code=400, detail="Tipo de atuador desconhecido.")


    thread = threading.Thread(target=_ligar_atuador, args=(tipo, endereco,), daemon=True)
    thread.start()

    return {"mensagem": f"processando."}

@app.post("/api/atuadores/desligar")
def desligar_atuador(comando: AtuadorComando):
    """ Desliga um atuador específico pelo tipo e endereço. """

    print("[API] /atuadores/desligar ", comando)
    tipo = comando.tipo
    endereco = comando.endereco

    if tipo not in [TIPO_AR_CONDICIONADO, TIPO_LAMPADA, TIPO_CONTROLE_INCENDIO]:
        raise HTTPException(status_code=400, detail="Tipo de atuador desconhecido.")

    stub = atua_manager.find_stub(tipo, endereco)
    if not stub:
        raise HTTPException(status_code=404, detail="Atuador não encontrado.")



    thread = threading.Thread(target=_desligar_atuador, args=(tipo, endereco,), daemon=True)
    thread.start()

    return {"mensagem": f"processando."}

@app.get("/api/salas")
def listar_salas():
    """ Retorna todas as salas e, para cada sala, os sensores e atuadores nela. """
    salas = {}

    # Agrupar sensores por sala
    for sensor in sensores_manager.listar_sensores():
        sala = sensor["sala"]
        if sala not in salas:
            salas[sala] = {"sensores": [], "atuadores": []}
        salas[sala]["sensores"].append(sensor)

    # Agrupar atuadores por sala
    for atuador in atua_manager.atuadores():
        sala = atuador["sala"]
        if sala not in salas:
            salas[sala] = {"sensores": [], "atuadores": []}
        salas[sala]["atuadores"].append({
            "tipo": atuador["tipo"],
            "endereco": atuador["endereco"],
            "ligado": atuador["ligado"],
            "adicional": atuador.get("adicional"),
            "auto_mode": atuador["auto_mode"]
        })

    return salas

@app.get("/api/decisoes")
def listar_descicoes():
    """ Retorna ultimas as decisões tomadas pelo sistema. """
    return {"decisoes": dmanager.get_decisoes()}

@app.post("/api/atuadores/mudar_modo")
def mudar_modo_atuador(comando: ModoAtuadorComando):
    """ Ativa ou desativa o controle automático de um atuador. """
    endereco = comando.endereco
    auto_mode = comando.auto_mode

    if atua_manager.definir_modo_atuador(endereco, auto_mode):
        estado = "automático" if auto_mode else "manual"
        return {"mensagem": f"Modo do atuador em {endereco} alterado para {estado}."}
    else:
        raise HTTPException(status_code=404, detail="Atuador não encontrado.")

def _desligar_atuador(tipo, endereco):
    if tipo == TIPO_AR_CONDICIONADO:
        atua_manager.desligar_ar_condicionado(endereco)
    elif tipo == TIPO_LAMPADA:
        atua_manager.desligar_lampada(endereco)
    elif tipo == TIPO_CONTROLE_INCENDIO:
        atua_manager.desativar_controle_incendio(endereco)
    
    atua_manager.atualizar_status_atuadores()
    
def _ligar_atuador(tipo, endereco):
    if tipo == TIPO_AR_CONDICIONADO:
        atua_manager.ligar_ar_condicionado(endereco)
    elif tipo == TIPO_LAMPADA:
        atua_manager.ligar_lampada(endereco)
    elif tipo == TIPO_CONTROLE_INCENDIO:
        atua_manager.ativar_controle_incendio(endereco)
    
    atua_manager.atualizar_status_atuadores()


@app.post("/api/atuadores/set_temperatura")
def set_temperatura_ar_condicionado(comando: SetTemperaturaComando):
    """ Ajusta a temperatura de um ar-condicionado específico. """
    endereco = comando.endereco
    temperatura = comando.temperatura

    if not atua_manager.validar_atuador(TIPO_AR_CONDICIONADO, endereco):
        raise HTTPException(status_code=404, detail="Ar-condicionado não encontrado.")

    atua_manager.set_temperatura_ar_condicionado(endereco, temperatura)
    atua_manager.atualizar_status_atuadores()
    return {"mensagem": f"Temperatura do ar-condicionado em {endereco} ajustada para {temperatura}°C."}



def iniciar_api():
    """ Inicia a API REST do FastAPI. """
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

if __name__ == "__main__":
    iniciar_api()
