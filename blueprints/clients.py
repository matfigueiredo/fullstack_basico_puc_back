from flask import Blueprint, request, jsonify
from models import db, Client, ClientAttribute, client_schema, clients_schema, attribute_schema, attributes_schema

clients_bp = Blueprint('clients', __name__, url_prefix='/api/clients')

@clients_bp.route('', methods=['GET'])
def get_clients():
    """Retorna lista de todos os clientes cadastrados."""
    clients = Client.query.all()
    return jsonify(clients_schema.dump(clients)), 200

@clients_bp.route('/<int:id>', methods=['GET'])
def get_client(id):
    """Retorna dados de um cliente específico."""
    client = Client.query.get(id)
    if not client:
        return jsonify({"message": "Cliente não encontrado"}), 404
    return jsonify(client_schema.dump(client)), 200

@clients_bp.route('', methods=['POST'])
def create_client():
    """Cria um novo cliente."""
    data = request.get_json()
    
    if not data or not data.get('name') or not data.get('email'):
        return jsonify({"message": "Dados incompletos. Nome e email são obrigatórios."}), 400
    
    client = Client(
        name=data.get('name'),
        email=data.get('email'),
        phone=data.get('phone', '')
    )
    
    try:
        db.session.add(client)
        db.session.commit()
        
        if 'attributes' in data and isinstance(data['attributes'], list):
            for attr_data in data['attributes']:
                if 'key' in attr_data and 'value' in attr_data:
                    attribute = ClientAttribute(
                        key=attr_data['key'],
                        value=attr_data['value'],
                        client_id=client.id
                    )
                    db.session.add(attribute)
            db.session.commit()
        
        return jsonify(client_schema.dump(client)), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Erro ao criar cliente: {str(e)}"}), 400

@clients_bp.route('/<int:id>', methods=['PUT'])
def update_client(id):
    """Atualiza dados de um cliente existente."""
    client = Client.query.get(id)
    if not client:
        return jsonify({"message": "Cliente não encontrado"}), 404
    
    data = request.get_json()
    
    if 'name' in data:
        client.name = data['name']
    if 'email' in data:
        client.email = data['email']
    if 'phone' in data:
        client.phone = data['phone']
    
    try:
        if 'attributes' in data and isinstance(data['attributes'], list):
            for attribute in client.attributes:
                db.session.delete(attribute)
            
            for attr_data in data['attributes']:
                if 'key' in attr_data and 'value' in attr_data:
                    attribute = ClientAttribute(
                        key=attr_data['key'],
                        value=attr_data['value'],
                        client_id=client.id
                    )
                    db.session.add(attribute)
        
        db.session.commit()
        return jsonify(client_schema.dump(client)), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Erro ao atualizar cliente: {str(e)}"}), 400

@clients_bp.route('/<int:id>', methods=['DELETE'])
def delete_client(id):
    """Remove um cliente."""
    client = Client.query.get(id)
    if not client:
        return jsonify({"message": "Cliente não encontrado"}), 404
    
    try:
        db.session.delete(client)
        db.session.commit()
        return jsonify({"message": "Cliente removido com sucesso"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Erro ao remover cliente: {str(e)}"}), 400

@clients_bp.route('/<int:id>/attributes', methods=['GET'])
def get_client_attributes(id):
    """Retorna atributos de um cliente."""
    client = Client.query.get(id)
    if not client:
        return jsonify({"message": "Cliente não encontrado"}), 404
    
    return jsonify(attributes_schema.dump(client.attributes)), 200

@clients_bp.route('/<int:id>/attributes', methods=['POST'])
def add_client_attribute(id):
    """Adiciona um novo atributo a um cliente."""
    client = Client.query.get(id)
    if not client:
        return jsonify({"message": "Cliente não encontrado"}), 404
    
    data = request.get_json()
    
    if not data or not data.get('key') or not data.get('value'):
        return jsonify({"message": "Dados incompletos. Chave e valor são obrigatórios."}), 400
    
    attribute = ClientAttribute(
        key=data.get('key'),
        value=data.get('value'),
        client_id=id
    )
    
    try:
        db.session.add(attribute)
        db.session.commit()
        return jsonify(attribute_schema.dump(attribute)), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Erro ao adicionar atributo: {str(e)}"}), 400 