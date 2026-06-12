from app import create_app
from app.models import WeeklyAttendance, Professional, PlanningWeek

app = create_app()
app.app_context().push()

# ??ltima semana importada
w = PlanningWeek.query.order_by(PlanningWeek.id.desc()).first()
print(f'??ltima semana: {w.week_label} (ID {w.id})')
print(f'Projeto: {w.project.name}')

# Registros dessa semana
atts = WeeklyAttendance.query.filter_by(planning_week_id=w.id).all()
print(f'\nRegistros de presen??a: {len(atts)}')

for att in atts:
    print(f'\n{att.professional.name} (MG{att.professional.registration}):')
    print(f'  Segunda: {att.monday_status}')
    if att.monday_activities:
        print(f'  Atividades: {att.monday_activities[:100]}...')
    else:
        print(f'  Atividades: VAZIO')
