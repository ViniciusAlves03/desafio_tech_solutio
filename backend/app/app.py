from flask import Flask
import os

from app.models.product_model import Product
from app.models.user_model import User

from app.utils.db import db
from app.utils.jwt_config import jwt
from app.utils.redis_client import redis_conn

from app.routes.product_routes import product_bp
from app.routes.user_routes import user_bp
from app.routes.auth_routes import auth_bp

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY", "secretjv123")

    db.init_app(app)
    jwt.init_app(app)

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
