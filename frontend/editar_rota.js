// Pega o ID da rota da URL
const urlParams = new URLSearchParams(window.location.search);
const rotaId = urlParams.get("id");

if (!rotaId) {
    alert("ID da rota não fornecido.");
    window.location.href = "admin.html";
}

// Inicialização do mapa
const map = L.map('map').setView([-2.4385, -54.6996], 13); // Posição inicial (Santarém, Pará)

// Adicionar camada do OpenStreetMap
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 18,
}).addTo(map);

// Inicialização do Leaflet Draw
const drawnItems = new L.FeatureGroup();
map.addLayer(drawnItems);

const drawControl = new L.Control.Draw({
    draw: {
        polyline: true,
        polygon: false,
        circle: false,
        rectangle: false,
        marker: false
    },
    edit: {
        featureGroup: drawnItems
    }
});
map.addControl(drawControl);

// Obter o token do administrador logado
const token = localStorage.getItem("token");

if (!token) {
    alert("Você precisa estar logado para editar uma rota!");
    window.location.href = "login.html";
}

// Buscar dados da rota para edição
async function carregarRota() {
    try {
        const response = await fetch(`http://127.0.0.1:8000/api/rotas/${rotaId}`, {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        if (!response.ok) {
            throw new Error("Erro ao carregar rota.");
        }

        const rota = await response.json();

        // Preencher o campo do nome do ônibus
        document.getElementById("nomeOnibus").value = rota.nome;

        // Adicionar a rota no mapa
        if (rota.pontos && rota.pontos.length > 0) {
            const latLngs = rota.pontos.map(ponto => [ponto.lat, ponto.lng]);
            const polyline = L.polyline(latLngs, { color: 'blue' }).addTo(drawnItems);
            map.fitBounds(polyline.getBounds()); // Ajustar o zoom do mapa para a rota carregada
        }
    } catch (error) {
        console.error("Erro ao carregar rota:", error);
        alert("Erro ao carregar os dados da rota.");
    }
}

// Carregar a rota ao iniciar a página
carregarRota();

// Evento ao criar uma nova rota no mapa
map.on(L.Draw.Event.CREATED, function (event) {
    const layer = event.layer;
    drawnItems.clearLayers(); // Remove a rota anterior
    drawnItems.addLayer(layer);
});

// Função para salvar a edição da rota
document.getElementById("rotaForm").addEventListener("submit", async function (event) {
    event.preventDefault();

    const nomeOnibus = document.getElementById("nomeOnibus").value.trim();

    // Verificar se o nome do ônibus foi preenchido
    if (!nomeOnibus) {
        alert("Por favor, insira o nome do ônibus.");
        return;
    }

    // Verificar se há uma rota desenhada
    if (drawnItems.getLayers().length === 0) {
        alert("Por favor, desenhe uma rota no mapa.");
        return;
    }

    // Obter as coordenadas da rota desenhada
    const layer = drawnItems.getLayers()[0]; // Obtém a camada desenhada

    // Verifica se a camada é uma linha (rota)
    if (!layer.getLatLngs) {
        alert("Desenhe uma linha para salvar a rota!");
        return;
    }

    const latLngs = layer.getLatLngs(); // Pega as coordenadas da linha

    // Se for um array dentro de outro, pega o primeiro array interno
    const rotaCoords = Array.isArray(latLngs[0]) ? latLngs[0].map(coord => ({
        lat: coord.lat,
        lng: coord.lng
    })) : latLngs.map(coord => ({
        lat: coord.lat,
        lng: coord.lng
    }));

    // ✅ Adicionar console.log() para verificar os dados que estão sendo enviados ao backend
    console.log("Token utilizado:", token);
    console.log("Dados enviados para a API:", JSON.stringify({
        nome: nomeOnibus,
        pontos: rotaCoords
    }));

    // Enviar a rota editada para o backend
    try {
        const response = await fetch(`http://127.0.0.1:8000/api/rotas/${rotaId}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({
                nome: nomeOnibus,
                pontos: rotaCoords
            })
        });

        const responseData = await response.json();
        
        if (response.ok) {
            alert("Rota editada com sucesso!");
            window.location.href = "admin.html";
        } else {
            console.error("Erro no backend:", responseData);
            alert(responseData.detail || "Erro ao editar a rota.");
        }
    } catch (error) {
        console.error("Erro ao conectar com o servidor:", error);
        alert("Erro ao conectar com o servidor.");
    }
});
