from flask import Flask
from dotenv import load_dotenv

load_dotenv()

from artist_hub.extensions import db, migrate
from artist_hub.config import (
    DevelopmentConfig,
    TestingConfig,
    ProductionConfig
)

config_map = {
    "dev": DevelopmentConfig,
    "test": TestingConfig,
    "prod": ProductionConfig
}


def create_app(config_name="dev"):
    app = Flask(__name__)
    app.config.from_object(config_map[config_name])
    
    print("DB URI:", app.config["SQLALCHEMY_DATABASE_URI"])
    print("JWT:", app.config["JWT_SECRET_KEY"])
    db.init_app(app)
    migrate.init_app(app, db)

    return app
