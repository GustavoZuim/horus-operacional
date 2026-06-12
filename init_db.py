"""
Script de inicializaÜÜo do banco de dados
Limpa todos os dados e cria um usuÜrio admin padrão
"""
from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash
import os

def init_database():
    """Limpa e inicializa o banco de dados"""
    app = create_app()
    
    with app.app_context():
        print('ÜÜÜ?  Limpando banco de dados...')
        
        # Remover arquivo do banco se existir
        if os.path.exists('horus.db'):
            os.remove('horus.db')
            print('   Ü? Banco antigo removido')
        
        # Criar todas as tabelas
        print('\nÜÜ Criando estrutura do banco...')
        db.create_all()
        print('   Ü? Tabelas criadas')
        
        # Criar usuÜrio admin padrão
        print('\nÜÜ Criando usuÜrio administrador...')
        admin = User(
            name='Administrador',
            email='admin@horus.local',
            password_hash=generate_password_hash('admin123'),
            role='admin',
            active=True
        )
        
        db.session.add(admin)
        db.session.commit()
        
        print('   Ü? Admin criado com sucesso!')
        print('\n' + '='*60)
        print('Ü? BANCO DE DADOS INICIALIZADO COM SUCESSO!')
        print('='*60)
        print('\nÜÜ Credenciais de acesso:')
        print('   Email:   admin@horus.local')
        print('   Senha:   admin123')
        print('\nÜÜÜ  IMPORTANTE: Altere a senha apÜs o primeiro login!')
        print('='*60)

if __name__ == '__main__':
    init_database()
