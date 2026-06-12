from app import create_app, db
from app.models import PlanningWeek, WeeklyAttendance, Holiday

app = create_app()
app.app_context().push()

w = PlanningWeek.query.filter_by(week_label='Semana 25').first()
if w:
    print(f'Deletando Semana 25 (ID {w.id})...')
    Holiday.query.filter_by(planning_week_id=w.id).delete()
    WeeklyAttendance.query.filter_by(planning_week_id=w.id).delete()
    db.session.delete(w)
    db.session.commit()
    print('Ü? Semana 25 deletada com sucesso')
else:
    print('Semana 25 nÜo encontrada')
