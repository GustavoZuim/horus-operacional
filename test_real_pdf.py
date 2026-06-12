# -*- coding: utf-8 -*-
"""
Teste do parser com o PDF real
"""
import sys
sys.path.insert(0, 'C:\\Users\\Gustavo\\Desktop\\horus-operacional')

from app.ai_parser import PlanningAIParser

# Caminho do PDF
pdf_path = r"C:\Users\Gustavo\Downloads\Planejamento Semanal - Educa Franco - Semana 25.pdf"

print("=" * 80)
print("TESTE DO PARSER COM PDF REAL")
print("=" * 80)

try:
    parser = PlanningAIParser(pdf_path)
    
    print(f"\n📄 PDF: {pdf_path}")
    print(f"📊 Total de páginas: {len(parser.pages_text)}")
    print(f"📝 Total de linhas: {len(parser.lines)}")
    
    # Mostrar primeiras 30 linhas
    print("\n" + "=" * 80)
    print("PRIMEIRAS 30 LINHAS DO PDF:")
    print("=" * 80)
    for i, line in enumerate(parser.lines[:30], 1):
        print(f"{i:3d}: {line}")
    
    # Testar extração de projeto
    print("\n" + "=" * 80)
    print("NOME DO PROJETO EXTRAÍDO:")
    print("=" * 80)
    project_name = parser.extract_project_name()
    print(f"✅ {project_name}")
    
    # Testar extração de profissionais de cada página
    print("\n" + "=" * 80)
    print("PROFISSIONAIS POR PÁGINA:")
    print("=" * 80)
    
    for page_num, page_text in enumerate(parser.pages_text, 1):
        print(f"\n📄 PÁGINA {page_num}:")
        print("-" * 40)
        professionals = parser.extract_professionals_from_page(page_text)
        
        if professionals:
            for prof in professionals:
                print(f"  ✅ {prof['name']} - Matrícula: {prof['registration']}")
        else:
            print("  ❌ Nenhum profissional detectado")
            # Mostrar primeiras linhas para debug
            lines = [l.strip() for l in page_text.split('\n') if l.strip()][:10]
            print("     Primeiras 10 linhas:")
            for line in lines:
                print(f"       {line}")
    
    # Parse completo
    print("\n" + "=" * 80)
    print("PARSE COMPLETO:")
    print("=" * 80)
    result = parser.parse_full_planning([])
    
    print(f"\n📦 Projeto: {result['project_name']}")
    print(f"📅 Semana: {result['week_info']['week_label']}")
    print(f"👥 Profissionais encontrados: {len(result['professionals'])}")
    
    for i, prof in enumerate(result['professionals'], 1):
        print(f"\n{i}. {prof['name']} ({prof['registration']})")
        # Contar atividades
        total_acts = sum([
            len([a for a in prof.get(f'{day}_activities', '').split('\n') if a.strip()])
            for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
        ])
        print(f"   Total de atividades: {total_acts}")
    
    if result.get('alerts'):
        print("\n⚠️  ALERTAS:")
        for alert in result['alerts']:
            print(f"   - {alert}")
    
    if result.get('debug_info'):
        print("\n🐛 DEBUG INFO:")
        for key, value in result['debug_info'].items():
            if key == 'sample_lines':
                print(f"   {key}: (primeiras 10)")
                for line in value[:10]:
                    print(f"      {line}")
            else:
                print(f"   {key}: {value}")

except FileNotFoundError:
    print(f"❌ Arquivo não encontrado: {pdf_path}")
    print("Por favor, salve o PDF como 'Planejamento_Semana_25.pdf' na pasta Downloads")
except Exception as e:
    print(f"❌ ERRO: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)
