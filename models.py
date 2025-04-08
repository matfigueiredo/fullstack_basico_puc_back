from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from marshmallow import Schema, fields

db = SQLAlchemy()

class Client(db.Model):
    __tablename__ = 'clients'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    attributes = db.relationship('ClientAttribute', backref='client', lazy=True, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<Client {self.name}>'

class ClientAttribute(db.Model):
    __tablename__ = 'client_attributes'
    
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), nullable=False)
    value = db.Column(db.String(255), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    def __repr__(self):
        return f'<ClientAttribute {self.key}: {self.value}>'


class ClientAttributeSchema(Schema):
    id = fields.Int(dump_only=True)
    key = fields.Str(required=True)
    value = fields.Str(required=True)
    client_id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)

class ClientSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    phone = fields.Str()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    attributes = fields.List(fields.Nested(ClientAttributeSchema), dump_only=True)

client_schema = ClientSchema()
clients_schema = ClientSchema(many=True)
attribute_schema = ClientAttributeSchema()
attributes_schema = ClientAttributeSchema(many=True)
