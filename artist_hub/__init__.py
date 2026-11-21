from flask import Flask
from dotenv import load_dotenv
from artist_hub.health import health
from artist_hub import models
from artist_hub.routes import main

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
    
    
    

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(health)
    app.register_blueprint(main)

    return app
