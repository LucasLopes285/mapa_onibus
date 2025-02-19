document.getElementById("cadastroAdminForm").addEventListener("submit", async function (event) {
    event.preventDefault();

    const nome = document.getElementById("nome").value;
    const email = document.getElementById("email").value;
    const senha = document.getElementById("senha").value;

    const adminData = {
        nome: nome,
        email: email,
        senha: senha,
        tipo: "administrador" // Cadastro como administrador
    };

    // Obter o token do administrador logado
    const token = localStorage.getItem("token");

    if (!token) {
        alert("Você precisa estar logado como administrador para cadastrar outro administrador!");
        window.location.href = "login.html";
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:8000/api/usuarios/registro", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}` // Envia o token do administrador logado
            },
            body: JSON.stringify(adminData)
        });

        if (response.ok) {
            alert("Administrador cadastrado com sucesso!");
            window.location.href = "admin.html"; // Redirecionar para o painel administrativo
        } else {
            const errorData = await response.json();
            alert(errorData.detail || "Erro ao cadastrar administrador.");
        }
    } catch (error) {
        console.error("Erro ao conectar com o servidor:", error);
        alert("Erro ao conectar com o servidor.");
    }
});
