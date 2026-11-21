import os


class DevelopmentConfig:
    DEBUG = True
    TESTING = False

    JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]
    JWT_ACCESS_TOKEN_EXPIRES = int(
    os.environ.get("JWT_ACCESS_TOKEN_EXPIRES", "3600")
)
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///dev.db"
    )
    


class TestingConfig:
    DEBUG = False
    TESTING = True

    JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]
    JWT_ACCESS_TOKEN_EXPIRES = int(
    os.environ.get("JWT_ACCESS_TOKEN_EXPIRES", "3600")
)
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
   

class ProductionConfig:
    DEBUG = False
    TESTING = False

    JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]
    JWT_ACCESS_TOKEN_EXPIRES = int(
    os.environ.get("JWT_ACCESS_TOKEN_EXPIRES", "3600")
)
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
    
