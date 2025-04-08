import os
from flask import Flask
from flask_cors import CORS
from models import db
from config.config import config
from config.swagger import configure_swagger
from blueprints.clients import clients_bp

def create_app(config_name='default'):
    """Função factory para criar a aplicação Flask."""
    
    app = Flask(__name__)
    
    app.config.from_object(config[config_name])
    
    CORS(app)
    
    db.init_app(app)
    
    configure_swagger(app)
    
    app.register_blueprint(clients_bp)
    
    return app

if __name__ == '__main__':
    env = os.environ.get('FLASK_ENV', 'development')
    app = create_app(env)
    
    with app.app_context():
        db.create_all()
    
    app.run(host='0.0.0.0', port=5000)
