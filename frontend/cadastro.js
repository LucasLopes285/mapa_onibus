document.getElementById("cadastroForm").addEventListener("submit", async function (event) {
    event.preventDefault();

    const nome = document.getElementById("nome").value;
    const email = document.getElementById("email").value;
    const senha = document.getElementById("senha").value;

    const userData = {
        nome: nome,
        email: email,
        senha: senha,
        tipo: "usuario" // Cadastro padrão como usuário
    };

    try {
        const response = await fetch("http://127.0.0.1:8000/api/usuarios/registro", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(userData)
        });

        if (response.ok) {
            alert("Usuário cadastrado com sucesso!");
            window.location.href = "login.html"; // Redirecionar para a página de login
        } else {
            alert("Erro ao cadastrar usuário.");
        }
    } catch (error) {
        console.error("Erro ao conectar com o servidor:", error);
        alert("Erro ao conectar com o servidor.");
    }
});
