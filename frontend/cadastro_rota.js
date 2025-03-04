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

// Evento ao criar uma nova rota
map.on(L.Draw.Event.CREATED, function (event) {
    const layer = event.layer;
    drawnItems.addLayer(layer);
});

// Função para salvar a rota
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

    // Obter o token do administrador logado
    const token = localStorage.getItem("token");

    if (!token) {
        alert("Você precisa estar logado para cadastrar uma rota!");
        window.location.href = "login.html";
        return;
    }

    // ✅ Adicionar console.log() para verificar os dados que estão sendo enviados ao backend
    console.log("Token utilizado:", token);
    console.log("Dados enviados para a API:", JSON.stringify({
        nome: nomeOnibus,
        pontos: rotaCoords
    }));

    // Enviar a rota para o backend
    try {
        const response = await fetch("http://127.0.0.1:8000/api/rotas", {
            method: "POST",
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
            alert("Rota cadastrada com sucesso!");
            window.location.href = "admin.html";
        } else {
            console.error("Erro no backend:", responseData);
            alert(responseData.detail || "Erro ao cadastrar a rota.");
        }
    } catch (error) {
        console.error("Erro ao conectar com o servidor:", error);
        alert("Erro ao conectar com o servidor.");
    }
});
