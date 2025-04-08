# API de Gerenciamento de Clientes

API RESTful desenvolvida com Flask e SQLAlchemy para gerenciamento de clientes.

## Descrição

Esta API permite realizar operações de CRUD (Criar, Ler, Atualizar e Deletar) de clientes e seus dados relacionados.

## Instruções de Instalação

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes do Python)

### Passos para instalação

1. Clone este repositório:
```
git clone <URL-do-repositório>
cd backend
```

2. Instale as dependências:
```
pip install -r requirements.txt
```

3. Execute a aplicação:
```
python app.py
```

A API estará disponível em: http://localhost:5000

## Rotas da API

- `GET /api/clients` - Listar todos os clientes
- `GET /api/clients/<id>` - Buscar um cliente específico
- `POST /api/clients` - Cadastrar novo cliente
- `PUT /api/clients/<id>` - Atualizar dados de um cliente
- `DELETE /api/clients/<id>` - Remover um cliente

## Documentação

A documentação da API está disponível em http://localhost:5000/api/docs usando Swagger UI.
