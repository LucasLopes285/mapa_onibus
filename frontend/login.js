document.getElementById("loginForm").addEventListener("submit", function (event) {
    event.preventDefault(); // Impede o envio do formulário padrão

    let email = document.getElementById("email").value;
    let senha = document.getElementById("senha").value;

    fetch("http://127.0.0.1:8000/api/usuarios/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: email, senha: senha })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Falha no login. Verifique suas credenciais.");
        }
        return response.json();
    })
    .then(data => {
        if (data.access_token) {
            console.log("Token recebido:", data.access_token); // Verificar se o token foi recebido
            localStorage.setItem("token", data.access_token); // Salvar token no localStorage

            // Buscar informações do usuário logado
            fetch("http://127.0.0.1:8000/api/usuarios/me", {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${data.access_token}`, // Enviar token corretamente
                    "Content-Type": "application/json"
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error("Falha ao obter informações do usuário.");
                }
                return response.json();
            })
            .then(userData => {
                console.log("Dados do usuário:", userData); // Depuração
                if (userData.tipo === "administrador") {
                    window.location.href = "admin.html"; // Redirecionar para painel admin
                } else {
                    window.location.href = "index.html"; // Redirecionar para o mapa
                }
            })
            .catch(error => console.error("Erro ao obter informações do usuário:", error));
        } else {
            document.getElementById("mensagemErro").style.display = "block";
            document.getElementById("mensagemErro").innerText = "E-mail ou senha incorretos.";
        }
    })
    .catch(error => {
        console.error("Erro ao fazer login:", error);
        document.getElementById("mensagemErro").style.display = "block";
        document.getElementById("mensagemErro").innerText = "Erro ao conectar com o servidor.";
    });
});
