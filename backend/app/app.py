from flask import Flask
import os
from flasgger import Swagger

from app.infrastructure.database.utils import db
from app.infrastructure.security import jwt
from app.infrastructure.redis import redis_conn
from app.ui.controller import product_bp, user_bp, auth_bp

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY", "secretjv123")

    db.init_app(app)
    jwt.init_app(app)

    app.config['SWAGGER'] = {
        'title': 'Products API - Technical Challenge',
        'openapi': '3.0.0',
        'uiversion': 3
    }

    swagger_template = {
        "info": {
            "title": "Products API",
            "description": "Interactive API documentation with Redis queues and PostgreSQL.",
            "version": "1.0.0"
        },
        "components": {
            "securitySchemes": {
                "bearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT",
                    "description": "Enter the JWT token here (without the Bearer prefix)."
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
