// Variável global para armazenar o endereço da API
let API_URL = localStorage.getItem("api_url") || "http://localhost:8000";


// Elementos da página
const listaSalas = document.getElementById("lista-salas");

// Função para definir o endereço da API
function definirEnderecoAPI() {
    listaSalas.innerHTML = ""; // Limpa a lista
    
    const input = document.getElementById("api-url");
    const url = input.value.trim();

    if (url) {
        API_URL = url;
        localStorage.setItem("api_url", url); // Salva no localStorage
        alert(`Endereço da API definido para: ${url}`);
        carregarSalas(); // Atualiza a lista de salas com o novo endereço
    } else {
        alert("Por favor, insira um endereço válido.");
    }
}

// Função para carregar o endereço da API ao abrir a página
function carregarEnderecoAPI() {
    const input = document.getElementById("api-url");
    input.value = API_URL; // Preenche o campo com o endereço salvo
}

// Função para buscar e exibir salas
async function carregarSalas() {
    try {
        const response = await fetch(`${API_URL}/api/salas`);
        const salas = await response.json();

        listaSalas.innerHTML = ""; // Limpa a lista
        for (const sala in salas) {
            const divSala = document.createElement("div");
            divSala.className = "sala mb-4";
            divSala.innerHTML = `
                <h3>Sala: ${sala}</h3>
                <div class="sensores">
                    <h4>Sensores</h4>
                    <div class="row">
                        ${salas[sala].sensores.map(sensor => `
                            <div class="col-md-4">
                                <div class="card">
                                    <div class="card-body">
                                        <h5 class="card-title">${sensor.sensor_id}: ${sensor.tipo}</h5>
                                        <p class="card-text"><b>Valor:</b>${sensor.valor}</p>
                                        <p class="card-text"><b>Captura: </b>${ moment(new Date(sensor.timestamp * 1000)).format('MM/DD/YYYY HH:mm:SS')}</p>
                                    </div>
                                </div>
                            </div>
                        `).join("")}
                    </div>
                </div>
                <div class="atuadores">
                    <h4>Atuadores</h4>
                    <div class="row">
                        ${salas[sala].atuadores.map(atuador => `
                            <div class="col-md-4 mb-3">
                                <div class="atuador">
                                    <div><strong>${atuador.tipo}</strong> - ${atuador.endereco}</div>
                                    <div>Estado: <span class="${atuador.ligado ?'text-success':'text-secondary'}">${atuador.ligado ? "Ligado" : "Desligado"}</span></div>
                                    <div>Modo: ${atuador.auto_mode ? "Automático" : "Manual"}</div>
                                    <button class="btn btn-primary btn-sm mt-2" onclick="mudarModo('${atuador.endereco}', ${!atuador.auto_mode})">
                                        Mudar para ${atuador.auto_mode ? "Manual" : "Automático"}
                                    </button>
                                    <button class="btn btn-success btn-sm mt-2" onclick="controlarAtuador('${atuador.tipo}','${atuador.endereco}', 'ligar')" ${atuador.auto_mode ? "disabled" : ""}>
                                        Ligar
                                    </button>
                                    <button class="btn btn-danger btn-sm mt-2" onclick="controlarAtuador('${atuador.tipo}','${atuador.endereco}', 'desligar')" ${atuador.auto_mode ? "disabled" : ""}>
                                        Desligar
                                    </button>
                                    <!-- controle de temperatura: -->
                                    ${atuador.tipo === "ar-condicionado" ? `
                                        <div class="ajustar-temperatura mt-3">
                                            <input type="range" id="temperatura-${atuador.endereco}" min="15" max="30" value="${atuador.adicional || 0}" oninput="atualizarTemperatura('${atuador.endereco}')" ${atuador.auto_mode ? "disabled" : ""}>
                                            <span class="temperatura-valor" id="temperatura-valor-${atuador.endereco}">${atuador.adicional || 0}</span>°C
                                            <button class="btn btn-info btn-sm mt-2" onclick="ajustarTemperatura('${atuador.endereco}')" ${atuador.auto_mode ? "disabled" : ""}>Ajustar</button>
                                        </div>
                                    ` : ""}
                                </div>
                            </div>
                        `).join("")}
                    </div>
                </div>
            `;
            listaSalas.appendChild(divSala);
        }
    } catch (error) {
        console.error("Erro ao carregar salas:", error);
    }
}

// Função para carregar as decisões
async function carregarDecisoes() {
    try {
        const response = await fetch(`${API_URL}/api/decisoes`);
        const json = await response.json();
        // console.log(json);
        const decisoes = json.decisoes;

        const listaDecisoes = document.getElementById("lista-decisoes");
        listaDecisoes.innerHTML = ""; // Limpa a lista

        decisoes.forEach(decisao => {
            const li = document.createElement("li");
            li.className = "list-group-item";
            li.textContent = decisao;
            listaDecisoes.appendChild(li);
        });
    } catch (error) {
        console.error("Erro ao carregar decisões:", error);
    }
}


// Função para atualizar o valor exibido do slider
function atualizarTemperatura(endereco) {
    const slider = document.getElementById(`temperatura-${endereco}`);
    const valor = document.getElementById(`temperatura-valor-${endereco}`);
    valor.textContent = slider.value;
}

// Função para mudar o modo do atuador
async function mudarModo(endereco, auto_mode) {
    try {
        const response = await fetch(`${API_URL}/api/atuadores/mudar_modo`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ endereco, auto_mode }),
        });

        if (response.ok) {
            alert(`Modo do atuador alterado para ${auto_mode ? "Automático" : "Manual"}`);
            carregarSalas(); // Atualiza a lista de salas
        } else {
            const error = await response.json();
            alert(`Erro: ${error.detail}`);
        }
    } catch (error) {
        console.error("Erro ao mudar modo do atuador:", error);
    }
}
 
// Função para ligar/desligar atuadores
async function controlarAtuador(tipo, endereco, acao) {
    try {
        const response = await fetch(`${API_URL}/api/atuadores/${acao}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ tipo, endereco }), // Envia o tipo dinamicamente
        });

        if (response.ok) {
            alert(`Atuador ${acao === "ligar" ? "ligado" : "desligado"} com sucesso!`);
            carregarSalas(); // Atualiza a lista de salas
        } else {
            const error = await response.json();
            alert(`Erro: ${error.detail}`);
        }
    } catch (error) {
        console.error(`Erro ao ${acao} atuador:`, error);
    }
}

// Função para ajustar a temperatura do ar-condicionado
async function ajustarTemperatura(endereco) {
    const slider = document.getElementById(`temperatura-${endereco}`);
    const temperatura = parseFloat(slider.value);

    try {
        const response = await fetch(`${API_URL}/api/atuadores/set_temperatura`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ endereco, temperatura }),
        });

        if (response.ok) {
            alert(`Temperatura do ar-condicionado ajustada para ${temperatura}°C`);
            carregarSalas(); // Atualiza a lista de salas
        } else {
            const error = await response.json();
            alert(`Erro: ${error.detail}`);
        }
    } catch (error) {
        console.error("Erro ao ajustar temperatura:", error);
    }
}


// Carrega o endereço da API ao abrir a página
carregarEnderecoAPI();

// Carrega as salas ao abrir a página
carregarSalas();

// Carrega as decisões ao abrir a página
carregarDecisoes();

// Atualiza a página a cada 10 segundos
setInterval(carregarSalas, 10000);  

// Atualiza as decisões a cada 5 segundos
setInterval(carregarDecisoes, 5000); // 5000 milissegundos = 5 segundos