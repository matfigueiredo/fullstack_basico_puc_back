# API de Gerenciamento de Clientes

API RESTful desenvolvida com Flask e SQLAlchemy para gerenciamento de clientes e seus atributos customizados.

![Versão](https://img.shields.io/badge/versão-1.0.0-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![Flask](https://img.shields.io/badge/Flask-2.0+-lightgrey)

## Descrição

Esta API permite realizar operações de CRUD (Criar, Ler, Atualizar e Deletar) de clientes e seus dados relacionados. O sistema foi projetado para ser facilmente extensível e integrado com outros serviços.

### Principais funcionalidades
- Gerenciamento completo de clientes
- Suporte para atributos customizáveis por cliente
- Documentação interativa via Swagger
- Respostas JSON padronizadas
- Tratamento de erros consistente

## Tecnologias utilizadas

- **Flask**: Framework web leve e flexível
- **SQLAlchemy**: ORM para manipulação do banco de dados
- **Marshmallow**: Serialização e validação de dados
- **Flask-Swagger**: Documentação interativa da API
- **SQLite**: Banco de dados (configurável para outros SGBDs)

## Estrutura do projeto

```
backend/
├── app.py              # Ponto de entrada da aplicação
├── config.py           # Configurações da aplicação
├── models.py           # Modelos de dados e schemas
├── blueprints/         # Rotas da API organizadas por recursos
│   ├── clients.py      # Endpoints de clientes
│   └── ...
├── static/             # Arquivos estáticos
│   └── swagger.json    # Documentação da API
```

## Instruções de Instalação

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes do Python)
- Ambiente virtual (recomendado)

### Passos para instalação

1. Clone este repositório:
```bash
git clone <URL-do-repositório>
cd backend
```

2. Crie e ative um ambiente virtual (opcional, mas recomendado):
```bash
python -m venv venv
# No Windows
venv\Scripts\activate
# No Linux/MacOS
source venv/bin/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente (opcional):
```bash
# No Windows
set FLASK_APP=app.py
set FLASK_ENV=development
# No Linux/MacOS
export FLASK_APP=app.py
export FLASK_ENV=development
```

5. Execute a aplicação:
```bash
python app.py
# Ou alternativamente
flask run
```

A API estará disponível em: http://localhost:5000

## Rotas da API

### Clientes
- `GET /api/clients` - Listar todos os clientes
- `GET /api/clients/<id>` - Buscar um cliente específico (incluindo seus atributos)
- `POST /api/clients` - Cadastrar novo cliente
- `PUT /api/clients/<id>` - Atualizar dados de um cliente
- `DELETE /api/clients/<id>` - Remover um cliente

### Atributos de clientes
- `POST /api/clients/<id>/attributes` - Adicionar um novo atributo a um cliente

## Exemplos de uso

### Criar um novo cliente
```bash
curl -X POST http://localhost:5000/api/clients \
  -H "Content-Type: application/json" \
  -d '{
    "name": "João Silva",
    "email": "joao.silva@exemplo.com",
    "phone": "(11) 98765-4321",
    "attributes": [
      {"key": "categoria", "value": "premium"},
      {"key": "região", "value": "sudeste"}
    ]
  }'
```

### Buscar um cliente
```bash
curl -X GET http://localhost:5000/api/clients/1
```

## Documentação

A documentação interativa da API está disponível em http://localhost:5000/api/docs usando Swagger UI.

## Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Faça commit das suas alterações (`git commit -m 'Adiciona nova funcionalidade'`)
4. Faça push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a licença MIT.
