from app.ai_parser import PlanningAIParser
import os

pdf_files = [f for f in os.listdir('temp_uploads') if f.endswith('.pdf')]
if pdf_files:
    pdf_path = os.path.join('temp_uploads', pdf_files[0])
    parser = PlanningAIParser(pdf_path)
    
    text = parser.pages_text[0]
    
    # Procurar por dias da semana
    print('=== ESTRUTURA DO PDF ===\n')
    
    days = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira']
    
    for day in days:
        if day in text:
            idx = text.index(day)
            # Pegar 200 caracteres apÜs o dia
            snippet = text[idx:idx+200]
            print(f'{day}:')
            print(snippet.encode('utf-8', errors='replace').decode('utf-8'))
            print('\n---\n')
