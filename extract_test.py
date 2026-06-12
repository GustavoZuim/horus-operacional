from app.ai_parser import PlanningAIParser
import os

pdf_files = [f for f in os.listdir('temp_uploads') if f.endswith('.pdf')]
if pdf_files:
    pdf_path = os.path.join('temp_uploads', pdf_files[0])
    parser = PlanningAIParser(pdf_path)
    
    print('=== EXTRAÇÃO DE ATIVIDADES DA PÁGINA ===\n')
    
    # Pegar texto da primeira página (Mara)
    page_text = parser.pages_text[0]
    
    # Extrair todas as atividades
    activities = parser._extract_all_activities_from_page(page_text)
    
    print(f'Total de atividades encontradas: {len(activities)}')
    print('\nAtividades:')
    for i, act in enumerate(activities, 1):
        # Extrair apenas a categoria
        category = act.split(':')[0]
        print(f'{i}. {category}')
