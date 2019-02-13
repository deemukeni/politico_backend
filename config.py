import os

class BaseConfig:
    DEBUG = False

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    FLASK_ENV="development"
    DATABASE_URL = os.getenv("DATABASE_URL")

class TestingConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    DATABASE_URL = os.getenv("DATABASE_TEST_URL")

app_configurations = {
    "development": DevelopmentConfig,
    "testing": TestingConfig
}
