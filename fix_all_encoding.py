"""
Script para corrigir encoding UTF-8 em TODOS os arquivos do projeto
Corrige HTML e Python
"""
from pathlib import Path
import re

# Mapeamento completo de caracteres corrompidos
REPLACEMENTS = {
    # Caracteres acentuados
    "Hórus": "Hórus",
    "vê": "vê",
    "Formulário": "Formulário",
    "Informações": "Informações",
    "Usuários": "Usuários",
    "usuários": "usuários",
    "vigília": "vigília",
    "Ação": "Ação",
    "ações": "ações",
    "Rápido": "Rápido",
    "presença": "presença",
    "Operação": "Operação",
    "Faça": "Faça",
    "prévia": "prévia",
    "revisível": "revisível",
    "Início": "Início",
    "métricas": "métricas",
    "relatórios": "relatórios",
    "Relatório": "Relatório",
    "Estatísticas": "Estatísticas",
    "histórico": "histórico",
    "Governança": "Governança",
    "Análise": "Análise",
    "permissões": "permissões",
    "Índice": "Índice",
    "importação": "importação",
    "técnicas": "técnicas",
    "extração": "extração",
    "Agente de IA": "Agente de IA",
    "interpretação": "interpretação",
    "inteligente": "inteligente",
    "português": "português",
    "Organização": "Organização",
    "Formação": "Formação",
    "Elaboração": "Elaboração",
    "Vistoria à": "Vistoria à",
    "Técnico": "Técnico",
    "Reunião": "Reunião",
    "Atendimento": "Atendimento",
    "Manutenção": "Manutenção",
    "Método": "Método",
    "Descrição": "Descrição",
    "descrição": "descrição",
    "categoria": "categoria",
    "Validação": "Validação",
    "padrão": "padrão",
    "supervisão": "supervisão",
    "exceções": "exceções",
    "pré-visualização": "pré-visualização",
    "••••••••••••": "••••••••••••",
    "Mística": "Mística",
    "Místico": "Místico",
    "Místicos": "Místicos",
    "Egípcio": "Egípcio",
    "místico": "místico",
    "mística": "mística",
    "místicos": "místicos",
    "noturno egípcio": "noturno egípcio",
    "céu": "céu",
    "Índigo": "Índigo",
    "Fumaça": "Fumaça",
    "Primárias": "Primárias",
    "primárias": "primárias",
    "Navegação": "Navegação",
    "Página": "Página",
    "página": "página",
    "específica": "específica",
    "Matrícula": "Matrícula",
    "matrícula": "matrícula",
    "seção": "seção",
    "Seção": "Seção",
    "pública": "pública",
    "Número": "Número",
    "número": "número",
    "células": "células",
    "Estatística": "Estatística",
    "estatística": "estatística",
}

def fix_file_encoding(file_path, is_python=False):
    """Corrige o encoding de um arquivo"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        original = content
        for wrong, correct in REPLACEMENTS.items():
            content = content.replace(wrong, correct)
        
        if content != original:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f'  ✗ Erro: {e}')
        return False

def main():
    """Processa todos os arquivos"""
    base_dir = Path('.')
    fixed_count = 0
    
    # Processar arquivos HTML
    print("=== CORRIGINDO TEMPLATES HTML ===\n")
    templates_dir = base_dir / 'app' / 'templates'
    for html_file in templates_dir.rglob('*.html'):
        print(f'HTML: {html_file}')
        if fix_file_encoding(html_file):
            print('  ✓ Corrigido')
            fixed_count += 1
        else:
            print('  - Sem alterações')
    
    # Processar arquivos Python
    print("\n=== CORRIGINDO ARQUIVOS PYTHON ===\n")
    python_patterns = [
        'app/**/*.py',
        '*.py'
    ]
    
    for pattern in python_patterns:
        for py_file in base_dir.glob(pattern):
            if py_file.is_file() and '__pycache__' not in str(py_file):
                print(f'Python: {py_file}')
                if fix_file_encoding(py_file, is_python=True):
                    print('  ✓ Corrigido')
                    fixed_count += 1
                else:
                    print('  - Sem alterações')
    
    print(f'\n✅ {fixed_count} arquivos corrigidos!')

if __name__ == '__main__':
    main()
