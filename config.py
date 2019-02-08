class BaseConfig:
    DEBUG = False

class DevelopmentConfig(BaseConfig):
    DEBUG = True

class TestingConfig(BaseConfig):
    DEBUG = True
    TESTING = True

app_configurations = {
    "development": DevelopmentConfig,
    "testing": TestingConfig
}
