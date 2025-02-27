// Função para carregar a lista de ônibus
async function carregarOnibus() {
    const token = localStorage.getItem("token");

    if (!token) {
        alert("Você precisa estar logado para acessar esta página!");
        window.location.href = "login.html";
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:8000/api/onibus", {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json"
            }
        });

        if (!response.ok) {
            throw new Error("Erro ao carregar a lista de ônibus.");
        }

        const onibus = await response.json();

        // Preencher a tabela com os dados dos ônibus
        const tabelaOnibus = document.getElementById("tabelaOnibus");
        tabelaOnibus.innerHTML = "";

        onibus.forEach(o => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${o.id}</td>
                <td>${o.nome}</td>
                <td>${o.rota_id}</td>
                <td>
                    <div class="acao-btns"> 
                        <button class="edit-btn" onclick="editarRota(${o.rota_id})">Editar Rota</button>
                        <button class="delete-btn" onclick="excluirOnibus(${o.id})">Excluir</button>
                    </div>
                </td>
            `;
            tabelaOnibus.appendChild(row);
        });
    } catch (error) {
        console.error("Erro ao carregar a lista de ônibus:", error);
        alert("Erro ao carregar a lista de ônibus.");
    }
}

// Função para redirecionar para a página de edição da rota
function editarRota(rotaId) {
    if (!rotaId) {
        alert("Esse ônibus não tem uma rota associada!");
        return;
    }
    window.location.href = `editar_rota.html?id=${rotaId}`;
}

// Função para excluir um ônibus
async function excluirOnibus(onibusId) {
    const token = localStorage.getItem("token");

    if (confirm("Tem certeza que deseja excluir este ônibus?")) {
        try {
            const response = await fetch(`http://127.0.0.1:8000/api/onibus/${onibusId}`, {
                method: "DELETE",
                headers: {
                    "Authorization": `Bearer ${token}`,
                    "Content-Type": "application/json"
                }
            });

            if (!response.ok) {
                throw new Error("Erro ao excluir o ônibus.");
            }

            alert("Ônibus excluído com sucesso!");
            carregarOnibus(); // Recarregar a lista após a exclusão
        } catch (error) {
            console.error("Erro ao excluir o ônibus:", error);
            alert("Erro ao excluir o ônibus.");
        }
    }
}

// Carregar a lista de ônibus ao carregar a página
document.addEventListener("DOMContentLoaded", carregarOnibus);
