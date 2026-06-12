"""
Ponto de entrada da aplicação Hórus Operacional
"""
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=False)
