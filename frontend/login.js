document.getElementById("loginForm").addEventListener("submit", function (event) {
    event.preventDefault(); // Impede o envio do formulário padrão
    console.log("Botão de login clicado!");

    let email = document.getElementById("email").value;
    let senha = document.getElementById("senha").value;

    fetch("http://127.0.0.1:8000/api/usuarios/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: email, senha: senha })
    })
    .then(response => response.json())
    .then(data => {
        if (data.access_token) {
            localStorage.setItem("token", data.access_token); // Salvar token no navegador
            window.location.href = "index.html"; // Redirecionar para o mapa
        } else {
            document.getElementById("mensagemErro").style.display = "block";
        }
    })
    .catch(error => console.error("Erro ao fazer login:", error));
});
