"""
Script para corrigir encoding UTF-8 corrompido nos templates HTML
"""
from pathlib import Path

# Mapeamento de strings corrompidas -> strings corretas
REPLACEMENTS = {
    "Hórus": "Hórus",
    "vê": "vê",
    "Formulário": "Formulário",
    "Informações": "Informações",
    "Usuários": "Usuários",
    "usuários": "usuários",
    "vigília": "vigília",
    "Ação": "Ação",
    "ações": "ações",
    "••••••••••••": "••••••••••••",
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
}

def fix_file_encoding(file_path):
    """Corrige o encoding de um arquivo HTML"""
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        
        original = content
        for wrong, correct in REPLACEMENTS.items():
            content = content.replace(wrong, correct)
        
        if content != original:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"  ✗ Erro: {e}")
        return False

def main():
    """Processa todos os arquivos HTML"""
    templates_dir = Path("app/templates")
    fixed_count = 0
    
    for html_file in templates_dir.rglob("*.html"):
        print(f"Processando: {html_file}")
        if fix_file_encoding(html_file):
            print("  ✓ Corrigido")
            fixed_count += 1
        else:
            print("  - Sem alterações")
    
    print(f"\n✅ {fixed_count} arquivos corrigidos!")

if __name__ == "__main__":
    main()
