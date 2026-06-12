from app.ai_parser import PlanningAIParser
import os

# Pegar o PDF
pdf_files = [f for f in os.listdir('temp_uploads') if f.endswith('.pdf')]
if pdf_files:
    pdf_path = os.path.join('temp_uploads', pdf_files[0])
    
    parser = PlanningAIParser(pdf_path)
    
    # Ver o texto bruto da primeira página
    print('=== TEXTO BRUTO DA P??GINA 1 ===\n')
    print(parser.pages_text[0][:2000])  # Primeiros 2000 caracteres
    
    print('\n\n=== TESTE DE EXTRA????O DE ATIVIDADES ===\n')
    activities = parser.extract_activities_by_day(parser.pages_text[0])
    
    for day, acts in activities.items():
        print(f'\n{day.upper()}:')
        if acts:
            for act in acts:
                print(f'  - {act}')
        else:
            print('  (vazio)')
