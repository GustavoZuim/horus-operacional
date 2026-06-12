"""
Utilitários para inicialização do banco de dados
"""
from datetime import date
from app import db
from app.models import User, Project, Professional, PlanningWeek, WeeklyAttendance


def initialize_database(app):
    """Inicializa o banco com dados de exemplo"""
    with app.app_context():
        # Criar tabelas
        db.create_all()
        
        # Verificar se jÜ existe admin
        admin_exists = User.query.filter_by(email='admin@example.com').first()
        
        if not admin_exists:
            print('Criando dados iniciais...')
            
            # Criar usuário admin
            admin = User(
                name='Gustavo Zuim',
                email='admin@example.com',
                role='admin',
                active=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            
            # Criar supervisor
            supervisor = User(
                name='Nathani',
                email='nathani@example.com',
                role='supervisor',
                active=True
            )
            supervisor.set_password('nathani123')
            db.session.add(supervisor)
            
            # Criar visualizador
            viewer = User(
                name='Visualizador',
                email='visualizador@example.com',
                role='visualizador',
                active=True
            )
            viewer.set_password('visualizador123')
            db.session.add(viewer)
            
            # Commit users primeiro para ter IDs
            db.session.commit()
            
            # Criar projeto Educaita
            educaita = Project(
                name='Educaita',
                status='active'
            )
            db.session.add(educaita)
            db.session.commit()
            
            # Criar profissionais
            professionals = [
                Professional(
                    name='AndrÜ Luiz GuimarÜes',
                    registration='MI34',
                    project_id=educaita.id,
                    status='active'
                ),
                Professional(
                    name='Pamela Silva',
                    registration='p.silva',
                    project_id=educaita.id,
                    status='active'
                ),
                Professional(
                    name='Roberto Altamirano',
                    registration='r.altamirano',
                    project_id=educaita.id,
                    status='active'
                ),
            ]
            for prof in professionals:
                db.session.add(prof)
            
            db.session.commit()
            
            # Criar Semana 25
            week_25 = PlanningWeek(
                project_id=educaita.id,
                week_label='Semana 25',
                start_date=date(2026, 6, 15),  # Segunda-feira
                end_date=date(2026, 6, 19),    # Sexta-feira
                created_by=admin.id
            )
            db.session.add(week_25)
            db.session.commit()
            
            # Criar registros de presença para todos os profissionais
            # Todos começam como "Presente" de segunda a sexta
            for prof in professionals:
                attendance = WeeklyAttendance(
                    planning_week_id=week_25.id,
                    project_id=educaita.id,
                    professional_id=prof.id,
                    monday_status='Presente',
                    tuesday_status='Presente',
                    wednesday_status='Presente',
                    thursday_status='Presente',
                    friday_status='Presente',
                    updated_by=admin.id
                )
                db.session.add(attendance)
            
            db.session.commit()
            
            print('✓ Dados iniciais criados!')
            print('✓ Admin: admin@example.com / admin123 (Gustavo Zuim)')
            print('✓ Supervisor: nathani@example.com / nathani123 (Nathani)')
            print('✓ Visualizador: visualizador@example.com / visualizador123')
            print('✓ Projeto: Educaita')
            print('✓ Profissionais: 3 cadastrados')
            print('✓ Semana 25: 15/06/2026 a 19/06/2026 (todos presentes)')
        else:
            print('! Banco jÜ inicializado.')
