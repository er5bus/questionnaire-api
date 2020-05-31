import os


class Config:
    """
    Base Config
    """
    SECRET_KEY = os.getenv('SECRET_KEY', '<replace with a secret key>')

    JWT_ACCESS_TOKEN_EXPIRES = False
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access']
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "hard to guess string")
    JWT_PUBLIC_KEY = os.getenv("JWT_PUBLIC_KEY", "hard to guess string")
    JWT_PRIVATE_KEY = os.getenv("JWT_PRIVATE_KEY", "hard to guess string")
    JWT_ERROR_MESSAGE_KEY = 'message'

    MONGODB_SETTINGS = {
        'host': os.getenv('DATABASE_URL', '<replace it with a database url>'),
        'connect': False
    }
    SENTRY_CDN = os.getenv('SENTRY_CDN', '<replace it with a database url>')

    ROOT_USERNAME = os.getenv("ROOT_USERNAME", "hard to guess string")
    ROOT_PASSWORD = os.getenv("ROOT_PASSWORD", "hard to guess string")

    @classmethod
    def init_app(cls, app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    @classmethod
    def init_app(cls, app):
        # log to stderr
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)


class TestingConfig(Config):
    TESTING = True


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
