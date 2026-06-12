from app.ai_parser import PlanningAIParser
from app import create_app
from app.models import Professional
import os

app = create_app()
app.app_context().push()

pdf_files = [f for f in os.listdir('temp_uploads') if f.endswith('.pdf')]
if pdf_files:
    pdf_path = os.path.join('temp_uploads', pdf_files[0])
    parser = PlanningAIParser(pdf_path)
    
    # Simular parsing
    registered = Professional.query.filter_by(project_id=3, status='active').all()
    result = parser.parse_full_planning(registered)
    
    for prof in result['professionals']:
        print(f"\n=== {prof['name']} ===")
        
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
        day_names = ['Segunda', 'TerÜa', 'Quarta', 'Quinta', 'Sexta']
        
        for day, name in zip(days, day_names):
            acts = prof[f'{day}_activities'].split('\n') if prof[f'{day}_activities'] else []
            acts = [a for a in acts if a.strip()]
            print(f'{name}: {len(acts)} atividades')
            if acts:
                print(f'  Primeira: {acts[0][:60]}...')
