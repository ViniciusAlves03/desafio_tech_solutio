from flask import Flask
import os
from flasgger import Swagger

from app.infrastructure.database.models.product_model import Product
from app.infrastructure.database.models.user_model import User

from app.utils.db import db
from app.utils.jwt_config import jwt
from app.utils.redis_client import redis_conn

from app.ui.controller.product_routes import product_bp
from app.ui.controller.user_routes import user_bp
from app.ui.controller.auth_routes import auth_bp

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY", "secretjv123")

    db.init_app(app)
    jwt.init_app(app)

    app.config['SWAGGER'] = {
        'title': 'API de Produtos - Desafio Técnico',
        'openapi': '3.0.0',
        'uiversion': 3
    }

    swagger_template = {
        "info": {
            "title": "API de Produtos (Clean Architecture)",
            "description": "Documentação interativa da API com filas no Redis e PostgreSQL.",
            "version": "1.0.0"
        },
        "components": {
            "securitySchemes": {
                "bearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT",
                    "description": "Insira o token JWT aqui (sem o prefixo Bearer)."
                }
            }
        }
    }
    Swagger(app, template=swagger_template)

    @jwt.token_in_blocklist_loader
    def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
        jti = jwt_payload["jti"]
        token_in_redis = redis_conn.get(jti)
        return token_in_redis is not None

    app.register_blueprint(product_bp, url_prefix='/v1')
    app.register_blueprint(user_bp, url_prefix='/v1')
    app.register_blueprint(auth_bp, url_prefix='/v1/auth')

    with app.app_context():
        db.create_all()

    return app
