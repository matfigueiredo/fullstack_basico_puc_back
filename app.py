from flask import Flask, jsonify, request
from flask_cors import CORS
from flasgger import Swagger
from database_manager import DatabaseManager
from controller.challenge_controller import challenge_bp
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DB_URL", "sqlite:///boostme.db")

def create_app():
    app = Flask(__name__)
    
    app.config["CORS_HEADERS"] = "Content-Type"
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    Swagger(app, template={
        "info": {
            "title": "BoostMe API",
            "description": "A weekly challenge generator API",
            "version": "1.0.0"
        },
        "basePath": "/api/v1"
    })
    
    db = DatabaseManager(DATABASE_URL)
    
    with app.app_context():
        db.init_db()
        db.seed_db()
        
    app.db = db
    
    app.register_blueprint(challenge_bp, url_prefix='/api/v1')
    
    return app

if __name__ == "__main__":
    app = create_app()
    debug_mode = os.getenv("DEBUG", "False").lower() == "true"
    app.run(host="0.0.0.0", port=8080, debug=debug_mode)