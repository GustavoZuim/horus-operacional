"""
UtilitÜrios para inicializaÜÜo do banco de dados
"""
from app import db
from app.models import User, Project, Professional
from config import Config


def initialize_database(app):
    """Inicializa o banco com dados de exemplo"""
    with app.app_context():
        # Criar tabelas
        db.create_all()
        
        # Verificar se jÜ existe admin
        admin_exists = User.query.filter_by(email=app.config['ADMIN_EMAIL']).first()
        
        if not admin_exists:
            # Criar usuÜrio admin
            admin = User(
                email=app.config['ADMIN_EMAIL'],
                name=app.config['ADMIN_NAME'],
                role='admin',
                active=True
            )
            admin.set_password(app.config['ADMIN_PASSWORD'])
            db.session.add(admin)
            
            # Criar supervisor de exemplo
            supervisor = User(
                email='nathani@horus.local',
                name='Nathani',
                role='supervisor',
                active=True
            )
            supervisor.set_password('supervisor123')
            db.session.add(supervisor)
            
            # Criar visualizador de exemplo
            viewer = User(
                email='viewer@horus.local',
                name='Visualizador',
                role='visualizador',
                active=True
            )
            viewer.set_password('viewer123')
            db.session.add(viewer)
            
            # Criar projetos de exemplo
            projects = [
                Project(name='Educaita', code='EDU', active=True),
                Project(name='CaÜapava', code='CAC', active=True),
                Project(name='MairiporÜ', code='MAI', active=True),
                Project(name='Ilhabela', code='ILH', active=True),
            ]
            for project in projects:
                db.session.add(project)
            
            # Criar profissionais de exemplo
            professionals = [
                Professional(
                    name='AndrÜ Luiz GuimarÜes',
                    registration='MI34',
                    role_description='Reconhecimento facial / testes',
                    active=True
                ),
                Professional(
                    name='Pamela Silva',
                    registration='p.silva',
                    role_description='Administrador do sistema',
                    active=True
                ),
                Professional(
                    name='Roberto Altamirano',
                    registration='r.altamirano',
                    role_description='Administrador do sistema',
                    active=True
                ),
            ]
            for prof in professionals:
                db.session.add(prof)
            
            db.session.commit()
            print('Ü? Dados iniciais criados!')
            print(f'Ü? Admin: {app.config["ADMIN_EMAIL"]} / {app.config["ADMIN_PASSWORD"]}')
            print('Ü? Supervisor: nathani@horus.local / supervisor123')
            print('Ü? Visualizador: viewer@horus.local / viewer123')
        else:
            print('! Banco jÜ inicializado.')
