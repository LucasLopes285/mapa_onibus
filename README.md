# 🚌 Mapa Interativo de Ônibus

Este é um projeto para visualizar rotas e paradas de ônibus em um **mapa interativo**.

## 📌 Tecnologias Utilizadas
- **FastAPI** → Backend
- **PostgreSQL** → Banco de Dados
- **Leaflet.js** → Mapa Interativo
- **GitHub** → Controle de Versão
- **Python**: Instale a versão 3.6 ou superior do Python (https://www.python.org/downloads/).


## 🚀 Como Rodar o Projeto

1️⃣ **Clone o repositório**  
```bash
git clone git@github.com:LucasLopes285/mapa_onibus.git
cd mapa_onibus

2️⃣ Crie e ative o ambiente virtual
python3 -m venv env
No Linux --> source env/bin/activate
No Windows --> .\env\Scripts\Activate 
No Windows --> env\Scripts\activate.bat

3️⃣ Instale as dependências
pip install -r requirements.txt

4️⃣ Execute o servidor
uvicorn backend.app:app --reload

5️⃣ Acesse a API no navegador
Swagger UI: http://127.0.0.1:8000/docs
Abra o arquivo login.html
sou
📌 Funcionalidades
✅ Exibição de rotas e paradas de ônibus em um mapa interativo.
✅ Autenticação: Usuários comuns podem visualizar, administradores podem cadastrar rotas.
✅ Banco de dados PostgreSQL para armazenamento das rotas e usuários.


