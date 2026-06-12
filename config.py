"""
Configurações da aplicaÜÜo Hórus Operacional
"""
import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    """ConfiguraÜÜo base"""
    
    # Configurações bÜsicas
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
    
    # Database
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', f'sqlite:///{os.path.join(basedir, "horus.db")}')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # App info
    APP_NAME = os.getenv('APP_NAME', 'Hórus Operacional')
    APP_DESCRIPTION = os.getenv('APP_DESCRIPTION', 'O olho que vê a assiduidade')
    
    # Admin inicial
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin@horus.local')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin123')
    ADMIN_NAME = os.getenv('ADMIN_NAME', 'Administrador')


class DevelopmentConfig(Config):
    """ConfiguraÜÜo de desenvolvimento"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """ConfiguraÜÜo de produÜÜo"""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True  # Requer HTTPS


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
