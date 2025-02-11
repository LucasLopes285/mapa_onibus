document.addEventListener("DOMContentLoaded", function () {
    // Inicializar o mapa em Santarém, Pará
    var map = L.map('map').setView([-2.43849, -54.6996], 13);

    // Adicionar camada do OpenStreetMap
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    // Função para carregar as rotas do backend
    function carregarRotas() {
        fetch("http://127.0.0.1:8000/api/rotas")
            .then(response => response.json())
            .then(data => {
                data.forEach(rota => {
                    let pontos = rota.pontos.map(p => [p.lat, p.lng]); // Converter coordenadas
                    let polyline = L.polyline(pontos, { color: 'blue' }).addTo(map);
                    polyline.bindPopup(`<b>Rota:</b> ${rota.nome}`);
                });
            })
            .catch(error => console.error("Erro ao carregar rotas:", error));
    }

    // Função para carregar as paradas do backend
    function carregarParadas() {
        fetch("http://127.0.0.1:8000/api/paradas")
            .then(response => response.json())
            .then(data => {
                data.forEach(parada => {
                    let marker = L.marker([parada.coordenadas.lat, parada.coordenadas.lng])
                        .addTo(map)
                        .bindPopup(`<b>Parada:</b> ${parada.nome}<br>${parada.descricao}`);
                });
            })
            .catch(error => console.error("Erro ao carregar paradas:", error));
    }

    // Carregar rotas e paradas ao iniciar
    carregarRotas();
    carregarParadas();
});
