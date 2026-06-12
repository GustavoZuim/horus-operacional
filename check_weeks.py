from app import create_app
from app.models import PlanningWeek

app = create_app()
app.app_context().push()

weeks = PlanningWeek.query.all()
print('=== SEMANAS NO BANCO ===')
for w in weeks:
    print(f'ID {w.id}: {w.week_name} ({w.start_date} a {w.end_date})')
