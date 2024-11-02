import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()


class Configuration:
    DEBUG = False
    DB_ADMIN_USERNAME = os.environ.get("POSTGRES_USER")
    DB_ADMIN_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
    DB_PASSWORD = os.environ.get("POSTGRES_READONLY_PASSWORD")
    DB_USERNAME = os.environ.get("POSTGRES_READONLY")
    DB_DELETE_USERNAME = os.environ.get("POSTGRES_DELETE_USERNAME")
    DB_DELETE_PASSWORD = os.environ.get("POSTGRES_DELETE_PASSWORD")
    POSTGRES_DB = os.environ.get("POSTGRES_DB")
    POSTGRES_DB_TEST = os.environ.get("POSTGRES_DB_TEST")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    DATABASE_URL_READONLY = os.environ.get("DATABASE_URL_READONLY")
    TEST_DATABASE_URI = os.environ.get("DATABASE_URL_TEST")
    ENABLE_CORS = True
    FLASK_APP = "app.wsgi"
    JSON_SORT_KEYS = False
    SECRET_KEY = os.environ.get("SECRET_KEY")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)


class DevelopmentConfig(Configuration):
    DEBUG = True
    # Override or add development-specific configuration variables here


class LocalDevelopmentConfig(Configuration):
    DB_PASSWORD = os.environ.get("POSTGRES_READONLY_PASSWORD")
    DB_USERNAME = os.environ.get("POSTGRES_READONLY")
    DB_DELETE_USERNAME = os.environ.get("POSTGRES_DELETE_USERNAME")
    DB_DELETE_PASSWORD = os.environ.get("POSTGRES_DELETE_PASSWORD")
    POSTGRES_DB = os.environ.get("POSTGRES_DB")
    POSTGRES_DB_TEST = os.environ.get("POSTGRES_DB_TEST")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL_LOCAL")
    TEST_DATABASE_URI = os.environ.get("DATABASE_URL_TEST")
    DEBUG = True


class ProductionConfig(Configuration):
    # Override or add production-specific configuration variables here
    pass


class TestingConfig(Configuration):
    DB_USERNAME = os.environ.get("POSTGRES_USER")
    DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
    POSTGRES_DB_TEST = os.environ.get("POSTGRES_DB_TEST")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL_TEST")
    TEST_DATABASE_URI = os.environ.get("DATABASE_URL_TEST")
    TESTING = True


# Set the active configuration class based on an environment variable
app_config = {
    "development": DevelopmentConfig,
    "local_development": LocalDevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}
