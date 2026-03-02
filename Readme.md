# Desafio Tech Solutio - Sistema de Gestão de Produtos

![Angular](https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

Este é o repositório do **Desafio Tech Solutio**, o objetivo é desenvolver um sistema capaz de gerir produtos.

O projeto está dividido em duas partes principais: uma **API REST** construída com Python e Flask e o **Frontend** construído com Angular 21.

## ✨ Principais Funcionalidades

### 🔐 Autenticação e Autorização (JWT)
* Registo de novos usuários com validação de dados.
* Login com E-mail ou Username.
* Autenticação baseada em JWT com expiração.
* Proteção de rotas: usuários só podem modificar ou excluir os seus próprios produtos e perfis.

### 📦 Gestão de Produtos (CRUD)
* **Criação:** Permite adicionar novos produtos com nome, marca, preço, quantidade e **upload de imagem**.
* **Listagem:** Tabela de produtos paginada, com suporte a ordenação (crescente/decrescente) e filtros de pesquisa por nome e marca.
* **Atualização:** Edição completa dos detalhes do produto e substituição da imagem.
* **Visualização:** Interface dedicada para exibir os detalhes do produto e sua imagem.
* **Exclusão:** Remoção dos produtos do inventário.

### ⚙️ Processamento em Background (Worker)
* As operações de escrita de produtos (Criar, Atualizar, Excluir) não bloqueiam a API. Elas são enviadas para uma fila no **Redis** e processadas de forma assíncrona por um **Worker** dedicado.

### 👤 Gestão de Usuário
* Visualização, edição de dados (username, email, senha) e exclusão da própria conta.
* **Exclusão em Cascata:** Ao excluir uma conta, todos os produtos associados a ela são automaticamente removidos da base de dados para manter a integridade.

## 🚀 Tecnologias Utilizadas

**Frontend (Client-Side)**
* **Core:** Angular 21, TypeScript
* **Estilização:** SCSS
* **Gestão de Estado & Requisições:** RxJS, HttpClient
* **Formulários:** Reactive Forms

**Backend (Server-Side)**
* **Core:** Python 3.11, Flask
* **Banco de Dados:** PostgreSQL
* **ORM:** SQLAlchemy
* **Validação de Dados:** Marshmallow
* **Mensageria & Filas:** Redis
* **Segurança:** Flask-JWT-Extended, Werkzeug (Hashing de Senhas)
* **Documentação da API:** Flasgger (Swagger UI)

**Infraestrutura**
* Docker & Docker Compose

## 📋 Pré-requisitos

Para executar este projeto localmente da forma mais fácil, precisa apenas de ter o seguinte instalado na sua máquina:

* **Docker** e **Docker Compose**
* **Git**

*Não é necessário instalar Python, Node.js, PostgreSQL ou Redis na sua máquina local, o Docker tratará de toda a infraestrutura de forma isolada.*

## ⚙️ Instalação e Execução (Docker)

O projeto está configurado para iniciar toda a infraestrutura (Banco de Dados, Redis, API, Worker e Frontend) com um único comando.

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/ViniciusAlves03/desafio_tech_solutio.git
   cd desafio_tech_solutio
   ```

2.  **Configure as variáveis de ambiente:**
    Crie um arquivo `.env` na raiz do projeto, baseado no `.env.example`. Você pode usar o seguinte comando:
    ```bash
    cp .env.example .env
    ```

3.  **Inicie os Serviços com Docker Compose:**
    Execute o comando abaixo na raiz do projeto. O Docker irá baixar as imagens do Postgres e Redis, construir as imagens do Flask e Angular, e iniciar todos os containers.
    ```bash
    docker-compose up -d --build
    ```
---

## 🌐 Acesso aos Serviços

Com a execução dos containers, os serviços estarão nos seguintes endereços:
* **Frontend:** http://localhost:4200
* **Backend:**: http://localhost:5000/v1
* **Documentação Swagger:**: http://localhost:5000/v1/apidocs

## 🏗️ Estrutura do Projeto

```sh
backend/
├── app/
│   ├── application/     # Portas e Serviços
│   ├── di/              # Configuração de Injeção de Dependência
│   ├── infrastructure/  # Postgres, SQLAlchemy, Redis, Repositórios, Schemas
│   ├── ui/              # Controladores, Swagger e Tratamento de Exceções
│   ├── utils/           # Constantes e utilitários
│   └── app.py           # Configuração e inicialização do Flask
├── tests/               # Testes com Pytest
├── worker.py            # Worker dedicado a consumir a fila do Redis
├── Dockerfile
└── requirements.txt
```

```sh
frontend/
├── src/
│   ├── app/
│   │   ├── core/        # Guards (Auth), Interceptors, Services e Utilitários
│   │   ├── features/    # Módulos Auth: Login/Register e Products: List/Form
│   │   ├── app.ts       # Componente Root
│   │   └── app.routes.ts# Definição de Rotas
│   ├── styles.scss      # Estilos Globais
│   └── main.ts          # Ponto de entrada
├── Dockerfile
└── package.json
```

---

## 🧪 Executando os Testes (Backend)

O backend possui uma suite de testes unitários desenvolvida com pytest. Para executar os testes, abra um novo terminal enquanto o container do backend estiver ativo e execute:
```bash
docker-compose run --rm web pytest tests/ -v
```
Os testes que passarem e/ou falharem aparecerão no seu terminal.

---

## 🧑‍💻 Autor <a id="autor"></a>

<p align="center">Desenvolvido por Vinícius Alves <strong><a href="https://github.com/ViniciusAlves03">(eu)</a></strong>.</p>

---
