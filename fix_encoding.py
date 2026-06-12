"""
Script para corrigir encoding UTF-8 corrompido nos templates HTML
"""
from pathlib import Path

# Mapeamento de strings corrompidas -> strings corretas
REPLACEMENTS = {
    "H??rus": "Hórus",
    "v??": "vê",
    "Formul??rio": "Formulário",
    "Informa????es": "Informações",
    "Usu??rios": "Usuários",
    "vig??lia": "vigília",
    "A????o": "Ação",
    "a????es": "ações",
    "????????????????????????": "••••••••••••",
    "R??pido": "Rápido",
    "presen??a": "presença",
    "Opera????o": "Operação",
    "Fa??a": "Faça",
    "pr??via": "prévia",
    "revis??vel": "revisível",
    "In??cio": "Início",
    "m??tricas": "métricas",
    "relat??rios": "relatórios",
    "Relat??rio": "Relatório",
    "Estat??sticas": "Estatísticas",
    "hist??rico": "histórico",
    "Governan??a": "Governança",
    "An??lise": "Análise",
    "permiss??es": "permissões",
    "??ndice": "Índice",
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
