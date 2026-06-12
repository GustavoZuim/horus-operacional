"""
Script para popular o banco de dados com usuários de teste
"""
from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

def seed_database():
    """Cria usuários de teste no banco"""
    app = create_app()
    
    with app.app_context():
        # Criar estrutura se não existir
        db.create_all()
        print('✓ Estrutura do banco verificada')
        
        # Verificar se já existem usuários
        if User.query.first() is not None:
            print('⚠ Banco já tem usuários, pulando seed...')
            return
        
        # Criar usuários de teste
        users = [
            User(
                name='Administrador',
                email='admin@example.com',
                password_hash=generate_password_hash('admin123'),
                role='admin',
                active=True
            ),
            User(
                name='Nathani Silva',
                email='nathani@example.com',
                password_hash=generate_password_hash('nathani123'),
                role='supervisor',
                active=True
            ),
            User(
                name='Visualizador',
                email='visualizador@example.com',
                password_hash=generate_password_hash('visualizador123'),
                role='viewer',
                active=True
            )
        ]
        
        for user in users:
            db.session.add(user)
        
        db.session.commit()
        
        print('✓ Usuários de teste criados com sucesso!')
        print('\nCredenciais disponíveis:')
        print('  Admin: admin@example.com / admin123')
        print('  Supervisor: nathani@example.com / nathani123')
        print('  Visualizador: visualizador@example.com / visualizador123')

if __name__ == '__main__':
    seed_database()
