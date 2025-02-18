// Inicialização do mapa
const map = L.map('map').setView([-2.43849, -54.6996], 13); // Santarém, Pará

// Camada do OpenStreetMap
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

// FeatureGroup para armazenar a rota desenhada
const drawnItems = new L.FeatureGroup();
map.addLayer(drawnItems);

// Controles de desenho (linha para a rota e marcadores para as paradas)
const drawControl = new L.Control.Draw({
    draw: {
        polyline: true,    // Linha da rota
        marker: true       // Paradas
    },
    edit: {
        featureGroup: drawnItems
    }
});
map.addControl(drawControl);

// Evento: Quando uma nova forma é criada
map.on(L.Draw.Event.CREATED, function (event) {
    const layer = event.layer;
    drawnItems.addLayer(layer);
});

// Evento do formulário para salvar a rota
document.getElementById("rotaForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    const nomeOnibus = document.getElementById("nomeOnibus").value;

    // Capturar a linha da rota (polilinha)
    let rotaCoordenadas = [];

    drawnItems.eachLayer(function (layer) {
        if (layer instanceof L.Polyline) {
            // Captura coordenadas da linha da rota
            rotaCoordenadas = layer.getLatLngs().map(latlng => ({
                lat: latlng.lat,
                lng: latlng.lng
            }));
        }
    });

    // Verificações básicas
    if (!rotaCoordenadas.length) {
        alert("Por favor, desenhe o trajeto da rota no mapa.");
        return;
    }

    // Montando o corpo da requisição
    const rotaData = {
        nome: nomeOnibus,
        pontos: rotaCoordenadas
    };

    // Enviando os dados para o backend via API
    try {
        const response = await fetch("http://127.0.0.1:8000/api/rotas", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(rotaData)
        });

        if (response.ok) {
            alert("Rota cadastrada com sucesso!");
            window.location.href = "admin.html"; // Voltar ao painel administrativo
        } else {
            alert("Erro ao cadastrar a rota.");
        }
    } catch (error) {
        console.error("Erro ao conectar com o servidor:", error);
        alert("Erro ao conectar com o servidor.");
    }
});
