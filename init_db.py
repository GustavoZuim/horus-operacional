"""
Script de inicializa????o do banco de dados
Limpa todos os dados e cria um usu??rio admin padrão
"""
from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash
import os

def init_database():
    """Limpa e inicializa o banco de dados"""
    app = create_app()
    
    with app.app_context():
        print('???????  Limpando banco de dados...')
        
        # Remover arquivo do banco se existir
        if os.path.exists('horus.db'):
            os.remove('horus.db')
            print('   ??? Banco antigo removido')
        
        # Criar todas as tabelas
        print('\n???? Criando estrutura do banco...')
        db.create_all()
        print('   ??? Tabelas criadas')
        
        # Criar usu??rio admin padrão
        print('\n???? Criando usu??rio administrador...')
        admin = User(
            name='Administrador',
            email='admin@horus.local',
            password_hash=generate_password_hash('admin123'),
            role='admin',
            active=True
        )
        
        db.session.add(admin)
        db.session.commit()
        
        print('   ??? Admin criado com sucesso!')
        print('\n' + '='*60)
        print('??? BANCO DE DADOS INICIALIZADO COM SUCESSO!')
        print('='*60)
        print('\n???? Credenciais de acesso:')
        print('   Email:   admin@horus.local')
        print('   Senha:   admin123')
        print('\n??????  IMPORTANTE: Altere a senha ap??s o primeiro login!')
        print('='*60)

if __name__ == '__main__':
    init_database()
