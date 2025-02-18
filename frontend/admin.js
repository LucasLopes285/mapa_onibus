document.addEventListener("DOMContentLoaded", function () {
    const token = localStorage.getItem("token");
    if (!token) {
        window.location.href = "login.html"; // Redirecionar se não estiver logado
        return;
    }

    // Verificar se o usuário é administrador
    fetch("http://127.0.0.1:8000/api/usuarios/me", {
        method: "GET",
        headers: { "Authorization": `Bearer ${token}` }
    })
    .then(response => response.json())
    .then(data => {
        if (data.tipo !== "administrador") {
            alert("Acesso negado! Apenas administradores podem acessar esta página.");
            window.location.href = "index.html";
        }
    })
    .catch(error => console.error("Erro ao verificar usuário:", error));

    // Carregar dados ao iniciar
    carregarRotas();
    carregarParadas();

    document.getElementById("logout").addEventListener("click", function () {
        if (confirm("Tem certeza que deseja sair?")) { // Mensagem de confirmação
            localStorage.removeItem("token"); // Remove o token do navegador
            alert("Logout realizado com sucesso!"); // Feedback para o usuário
            window.location.href = "login.html"; // Redireciona para o login
        }
    });
    
});

// Função para carregar as rotas e exibi-las na tabela
function carregarRotas() {
    fetch("http://127.0.0.1:8000/api/rotas")
        .then(response => response.json())
        .then(data => {
            let tabela = document.getElementById("tabelaRotas");
            tabela.innerHTML = ""; // Limpa a tabela antes de recarregar
            data.forEach(rota => {
                let linha = `<tr>
                    <td>${rota.id}</td>
                    <td>${rota.nome}</td>
                    <td>${JSON.stringify(rota.pontos)}</td>
                    <td>
                        <button onclick="editarRota(${rota.id})">✏️ Editar</button>
                        <button onclick="excluirRota(${rota.id})">🗑️ Excluir</button>
                    </td>
                </tr>`;
                tabela.innerHTML += linha;
            });
        })
        .catch(error => console.error("Erro ao carregar rotas:", error));
}

// Função para carregar as paradas e exibi-las na tabela
function carregarParadas() {
    fetch("http://127.0.0.1:8000/api/paradas")
        .then(response => response.json())
        .then(data => {
            let tabela = document.getElementById("tabelaParadas");
            tabela.innerHTML = ""; // Limpa a tabela antes de recarregar
            data.forEach(parada => {
                let linha = `<tr>
                    <td>${parada.id}</td>
                    <td>${parada.nome}</td>
                    <td>${JSON.stringify(parada.coordenadas)}</td>
                    <td>${parada.descricao || "Sem descrição"}</td>
                    <td>
                        <button onclick="editarParada(${parada.id})">✏️ Editar</button>
                        <button onclick="excluirParada(${parada.id})">🗑️ Excluir</button>
                    </td>
                </tr>`;
                tabela.innerHTML += linha;
            });
        })
        .catch(error => console.error("Erro ao carregar paradas:", error));
}
