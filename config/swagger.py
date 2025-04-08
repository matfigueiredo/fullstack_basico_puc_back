from flask_swagger_ui import get_swaggerui_blueprint
import os
import json

def configure_swagger(app):
    """Configura o Swagger UI para a aplicação."""
    
    SWAGGER_URL = '/api/docs'
    API_URL = '/static/swagger.json'

    swagger_ui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "API de Gerenciamento de Clientes"
        }
    )

    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

    # Criação do diretório static para o arquivo swagger.json
    if not os.path.exists('static'):
        os.makedirs('static')

    swagger_data = {
        "swagger": "2.0",
        "info": {
            "title": "API de Gerenciamento de Clientes",
            "description": "API para operações CRUD de clientes",
            "version": "1.0.0"
        },
        "host": "localhost:5000",
        "basePath": "/api",
        "schemes": ["http"],
        "paths": {
            "/clients": {
                "get": {
                    "summary": "Listar todos os clientes",
                    "responses": {
                        "200": {
                            "description": "Lista de clientes"
                        }
                    }
                },
                "post": {
                    "summary": "Criar um novo cliente",
                    "parameters": [
                        {
                            "name": "body",
                            "in": "body",
                            "required": True,
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "name": {"type": "string"},
                                    "email": {"type": "string"},
                                    "phone": {"type": "string"},
                                    "attributes": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "key": {"type": "string"},
                                                "value": {"type": "string"}
                                            }
                                        }
                                    }
                                },
                                "required": ["name", "email"]
                            }
                        }
                    ],
                    "responses": {
                        "201": {
                            "description": "Cliente criado com sucesso"
                        },
                        "400": {
                            "description": "Dados inválidos"
                        }
                    }
                }
            },
            "/clients/{id}": {
                "get": {
                    "summary": "Buscar um cliente específico",
                    "parameters": [
                        {
                            "name": "id",
                            "in": "path",
                            "required": True,
                            "type": "integer"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Cliente encontrado"
                        },
                        "404": {
                            "description": "Cliente não encontrado"
                        }
                    }
                },
                "put": {
                    "summary": "Atualizar dados de um cliente",
                    "parameters": [
                        {
                            "name": "id",
                            "in": "path",
                            "required": True,
                            "type": "integer"
                        },
                        {
                            "name": "body",
                            "in": "body",
                            "required": True,
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "name": {"type": "string"},
                                    "email": {"type": "string"},
                                    "phone": {"type": "string"},
                                    "attributes": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "key": {"type": "string"},
                                                "value": {"type": "string"}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Cliente atualizado com sucesso"
                        },
                        "404": {
                            "description": "Cliente não encontrado"
                        }
                    }
                },
                "delete": {
                    "summary": "Remover um cliente",
                    "parameters": [
                        {
                            "name": "id",
                            "in": "path",
                            "required": True,
                            "type": "integer"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Cliente removido com sucesso"
                        },
                        "404": {
                            "description": "Cliente não encontrado"
                        }
                    }
                }
            },
            "/clients/{id}/attributes": {
                "post": {
                    "summary": "Adicionar atributo ao cliente",
                    "parameters": [
                        {
                            "name": "id",
                            "in": "path",
                            "required": True,
                            "type": "integer"
                        },
                        {
                            "name": "body",
                            "in": "body",
                            "required": True,
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "key": {"type": "string"},
                                    "value": {"type": "string"}
                                },
                                "required": ["key", "value"]
                            }
                        }
                    ],
                    "responses": {
                        "201": {
                            "description": "Atributo adicionado com sucesso"
                        },
                        "404": {
                            "description": "Cliente não encontrado"
                        }
                    }
                },
                "get": {
                    "summary": "Listar atributos do cliente",
                    "parameters": [
                        {
                            "name": "id",
                            "in": "path",
                            "required": True,
                            "type": "integer"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Lista de atributos"
                        },
                        "404": {
                            "description": "Cliente não encontrado"
                        }
                    }
                }
            }
        }
    }

    with open('static/swagger.json', 'w') as f:
        json.dump(swagger_data, f) 