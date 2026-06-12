"""
Factory da aplica????o Flask - Hórus Operacional
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import config

# Extens??es
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()


def create_app(config_name='development'):
    """Factory pattern para criar a aplica????o"""
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Inicializar extens??es
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    
    # Configurar Flask-Login
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Faça login para acessar esta página.'
    login_manager.login_message_category = 'warning'
    
    # Importar models antes dos blueprints
    from app import models
    
    # Registrar blueprints
    from app.routes import auth, main, users, projects, professionals, weekly, reports, logs, imports, activity_report
    
    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(users.bp)
    app.register_blueprint(projects.bp)
    app.register_blueprint(professionals.bp)
    app.register_blueprint(weekly.bp)
    app.register_blueprint(reports.bp)
    app.register_blueprint(logs.bp)
    app.register_blueprint(imports.bp)
    app.register_blueprint(activity_report.bp)
    
    # Criar tabelas se n??o existirem
    with app.app_context():
        db.create_all()
    
    return app
