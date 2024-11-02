import logging
import socket
from datetime import datetime, timezone
from pathlib import Path

import connexion
from flask import Flask, request
from flask_bcrypt import Bcrypt
from flask_compress import Compress
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

from alembic import command
from alembic.config import Config
from app.config import app_config
from app.datatypes import UserRoleEnum
from app.models import User

BASE = Path(__file__).resolve().parent


def get_nginx_ip():
    try:
        nginx_ip = socket.gethostbyname("dgg_nginx")
        return nginx_ip
    except socket.gaierror:
        return None


def is_exempt():
    nginx_ip = get_nginx_ip()
    return request.remote_addr == nginx_ip


db = SQLAlchemy()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["600/minute", "1000/hour", "10000/day"],
    strategy="fixed-window-elastic-expiry",
    storage_uri="",  # Set in create_app()
    storage_options={},
    default_limits_exempt_when=is_exempt,
)

bcrypt = Bcrypt()


def create_app(config_name: str) -> Flask:
    options = {"swagger_ui": True, "swagger_ui_config": {"syntaxHighlight": False}}
    connexion_app = connexion.FlaskApp(
        __name__, specification_dir="./",
        options=options
    )
    connexion_app.add_api("api-config.yaml", resolver=connexion.resolver.RelativeResolver("app.endpoints"))
    app = connexion_app.app
    app.config.from_object(app_config[config_name])
    app.config["ENV"] = config_name
    Compress(app)
    app.config["COMPRESS_ALWAYS"] = True
    db.init_app(app)
    bcrypt.init_app(app)
    _ = JWTManager(app)
    CORS(app, resources={r"/*": {"origins": "*"}})

    if not logging.getLogger().handlers:
        logging.basicConfig(level=logging.INFO)
        app.logger.addHandler(logging.StreamHandler())  # Log to the terminal
        log_path = BASE.parent.joinpath("api_logs.log")
        file_handler = logging.FileHandler(log_path)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
    if config_name not in ["local_development", "testing"]:
        limiter._storage_uri = "memcached://dgg_memcached:11211"
        limiter.init_app(app)
        upgrade_alembic(app)
    if config_name != "testing":
        create_users(app, db)

    # Revert to read-only database for read-only users after writing data
    app.config["SQLALCHEMY_DATABASE_URI"] = app.config["DATABASE_URL_READONLY"]

    @app.before_request
    def before_request_function():
        args = request.args
        app.logger.info(
            f"time={datetime.now(timezone.utc)}, url={request.url}, endpoint={request.path} params={dict(args.items())}"
        )

    @app.after_request
    def after_request_func(response):
        return response
    from .endpoints import api_bp
    app.register_blueprint(api_bp, url_prefix='/api/v2')
    return app


def create_users(app: Flask, db) -> None:
    admin_user = app.config["DB_ADMIN_USERNAME"]
    admin_password = app.config["DB_ADMIN_PASSWORD"]
    read_user = app.config["DB_USERNAME"]
    read_password = app.config["DB_PASSWORD"]
    delete_user = app.config["DB_DELETE_USERNAME"]
    delete_password = app.config["DB_DELETE_PASSWORD"]

    add_users_to_db(admin_user, admin_password, UserRoleEnum.WRITE, app, db)
    add_users_to_db(read_user, read_password, UserRoleEnum.READ, app, db)
    add_users_to_db(delete_user, delete_password, UserRoleEnum.DELETE, app, db)


def add_users_to_db(user_name: str, password: str, role: UserRoleEnum, app: Flask, db):
    with app.app_context():
        user = db.session.query(User).filter_by(username=user_name).first()
        if user:
            db.session.delete(user)
            db.session.commit()
        user = User(username=user_name, password=password, role=role)
        db.session.add(user)
        db.session.commit()


def upgrade_alembic(app: Flask):
    alembic_cfg = Config(BASE.parent.joinpath("alembic.ini"))
    alembic_cfg.set_main_option(
        "sqlalchemy.url",
        app.config["SQLALCHEMY_DATABASE_URI"],
    )
    command.upgrade(alembic_cfg, "head")
