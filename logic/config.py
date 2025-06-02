import os


class Config:
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

    SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'quiz-jwt-secret-change-in-production')

    ORACLE_HOST = os.getenv('ORACLE_HOST', 'localhost')
    ORACLE_PORT = int(os.getenv('ORACLE_PORT', '1521'))
    ORACLE_SERVICE_NAME = os.getenv('ORACLE_SERVICE_NAME', 'FREEPDB1')
    ORACLE_USERNAME = os.getenv('ORACLE_USERNAME', 'quiz_user')
    ORACLE_PASSWORD = os.getenv('ORACLE_PASSWORD', 'password')

    def DATABASE_URL(self) -> str:
        return f"oracle+oracledb://{self.ORACLE_USERNAME}:{self.ORACLE_PASSWORD}@{self.ORACLE_HOST}:{self.ORACLE_PORT}/?service_name={self.ORACLE_SERVICE_NAME}"


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'quiz-jwt-secret-dev')

    ORACLE_USERNAME = os.getenv('ORACLE_USERNAME', 'quiz_dev')
    ORACLE_PASSWORD = os.getenv('ORACLE_PASSWORD', 'dev_password')


class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = os.getenv('JWT_SECRET_KEY')

    ORACLE_HOST = os.getenv('ORACLE_HOST')
    ORACLE_USERNAME = os.getenv('ORACLE_USERNAME')
    ORACLE_PASSWORD = os.getenv('ORACLE_PASSWORD')
    ORACLE_SERVICE_NAME = os.getenv('ORACLE_SERVICE_NAME', 'PRODPDB1')


config_by_name = {
    'development': DevelopmentConfig(),
    'production': ProductionConfig()
}


def get_config():
    env = os.getenv('FLASK_ENV', 'development')
    config_class = config_by_name.get(env, DevelopmentConfig)

    if env == 'production':
        if not config_class.SECRET_KEY:
            raise ValueError("JWT_SECRET_KEY must be set in production")

        if not all([
            config_class.ORACLE_HOST,
            config_class.ORACLE_USERNAME,
            config_class.ORACLE_PASSWORD,
            config_class.ORACLE_SERVICE_NAME
        ]):
            raise ValueError("Oracle configuration must be set in production")

    return config_class