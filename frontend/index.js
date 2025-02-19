// Inicialização do mapa
const map = L.map('map').setView([-2.4385, -54.6996], 13); // Posição inicial (Santarém, Pará)

// Adicionar camada do OpenStreetMap
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 18,
}).addTo(map);

// Variável para armazenar a camada da rota atual
let rotaLayer = null;

// Função para buscar a rota pelo nome do ônibus
async function buscarRota(nomeOnibus) {
    try {
        const response = await fetch(`http://127.0.0.1:8000/api/onibus/nome/${nomeOnibus}`);
        if (!response.ok) {
            throw new Error("Rota não encontrada!");
        }
        const onibus = await response.json();
        
        // Obter a rota associada
        const rotaResponse = await fetch(`http://127.0.0.1:8000/api/rotas/${onibus.rota_id}`);
        if (!rotaResponse.ok) {
            throw new Error("Rota associada não encontrada!");
        }
        const rota = await rotaResponse.json();

        // Remover camada da rota anterior, se existir
        if (rotaLayer) {
            map.removeLayer(rotaLayer);
        }

        // Exibir a rota no mapa
        rotaLayer = L.polyline(rota.pontos.map(p => [p.lat, p.lng]), {
            color: 'blue',
            weight: 5,
        }).addTo(map);

        // Ajustar a visualização do mapa para a rota
        map.fitBounds(rotaLayer.getBounds());

    } catch (error) {
        console.error("Erro ao buscar a rota:", error);
        alert("Ônibus ou rota não encontrados!");
    }
}

// Evento do formulário de pesquisa
document.getElementById("pesquisaForm").addEventListener("submit", function (event) {
    event.preventDefault();
    const nomeOnibus = document.getElementById("nomeOnibus").value.trim();
    if (nomeOnibus) {
        buscarRota(nomeOnibus);
    }
});
