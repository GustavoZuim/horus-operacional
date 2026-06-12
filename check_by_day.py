from app import create_app
from app.models import WeeklyAttendance, Professional

app = create_app()
app.app_context().push()

# Pegar a Mara
att = WeeklyAttendance.query.filter_by(planning_week_id=1, professional_id=6).first()

if att:
    print(f'=== {att.professional.name} ===\n')
    
    days = {
        'Segunda': att.monday_activities,
        'Terça': att.tuesday_activities,
        'Quarta': att.wednesday_activities,
        'Quinta': att.thursday_activities,
        'Sexta': att.friday_activities
    }
    
    for day, activities in days.items():
        print(f'{day}:')
        if activities:
            acts = activities.split('\n')
            print(f'  Total: {len(acts)} atividades')
            for i, act in enumerate(acts[:2], 1):  # Mostrar sÜ 2
                print(f'  {i}. {act[:80]}...')
        else:
            print('  VAZIO')
        print()
