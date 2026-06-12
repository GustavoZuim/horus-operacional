"""
Rotas de relat??rio mensal de atividades
"""
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from datetime import datetime
from sqlalchemy import extract
from app import db
from app.models import Project, PlanningWeek, WeeklyAttendance
from collections import defaultdict

bp = Blueprint('activity_report', __name__, url_prefix='/activity-report')

# Tradu????o de meses para portugu??s
MONTHS_PT = {
    1: 'Janeiro', 2: 'Fevereiro', 3: 'Mar??o', 4: 'Abril',
    5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
    9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
}


def parse_activities(activities_text):
    """Extrai categorias das atividades"""
    if not activities_text:
        return []
    
    categories = []
    lines = activities_text.split('\n')
    
    for line in lines:
        line = line.strip()
        if ':' in line and line:
            category = line.split(':')[0].strip()
            if category and len(category) > 3:  # Filtrar categorias v??lidas
                categories.append(category)
    
    return categories


@bp.route('/')
@login_required
def index():
    """P??gina principal do relat??rio de atividades"""
    # Buscar projetos ativos
    projects = Project.query.filter_by(status='active').order_by(Project.name).all()
    
    # Buscar meses dispon??veis
    weeks = PlanningWeek.query.order_by(PlanningWeek.start_date.desc()).all()
    
    months = []
    seen_months = set()
    for week in weeks:
        month_key = week.start_date.strftime('%Y-%m')
        if month_key not in seen_months:
            seen_months.add(month_key)
            month_name = MONTHS_PT[week.start_date.month]
            year = week.start_date.year
            months.append({
                'value': month_key,
                'label': f'{month_name} de {year}'
            })
    
    return render_template('activity_report/index.html', projects=projects, months=months)


@bp.route('/data')
@login_required
def get_data():
    """Retorna dados do relat??rio de atividades"""
    month = request.args.get('month')  # Formato: YYYY-MM
    
    if not month:
        return jsonify({'error': 'M??s n??o especificado'}), 400
    
    try:
        year, month_num = map(int, month.split('-'))
    except:
        return jsonify({'error': 'Formato de m??s inv??lido'}), 400
    
    # Buscar todas as semanas do m??s
    weeks = PlanningWeek.query.filter(
        extract('year', PlanningWeek.start_date) == year,
        extract('month', PlanningWeek.start_date) == month_num
    ).all()
    
    if not weeks:
        return jsonify({
            'projects': [],
            'total_categories': [],
            'grand_total': 0,
            'month_label': datetime(year, month_num, 1).strftime('%B de %Y').capitalize()
        })
    
    # Estruturas para contagem
    project_data = defaultdict(lambda: defaultdict(int))
    total_categories = defaultdict(int)
    grand_total = 0
    
    # Processar cada semana
    for week in weeks:
        attendances = WeeklyAttendance.query.filter_by(planning_week_id=week.id).all()
        
        for att in attendances:
            # Processar cada dia da semana
            days = [
                att.monday_activities,
                att.tuesday_activities,
                att.wednesday_activities,
                att.thursday_activities,
                att.friday_activities
            ]
            
            for day_activities in days:
                if day_activities:
                    categories = parse_activities(day_activities)
                    
                    for category in categories:
                        project_data[week.project_id][category] += 1
                        total_categories[category] += 1
                        grand_total += 1
    
    # Montar resultado por projeto
    projects_result = []
    
    for project_id, categories in project_data.items():
        project = Project.query.get(project_id)
        
        # Ordenar categorias por quantidade (decrescente)
        sorted_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)
        
        project_total = sum(categories.values())
        
        projects_result.append({
            'id': project.id,
            'name': project.name,
            'categories': [{'name': cat, 'count': count} for cat, count in sorted_categories],
            'total': project_total
        })
    
    # Ordenar projetos por total de atividades (decrescente)
    projects_result.sort(key=lambda x: x['total'], reverse=True)
    
    # Ordenar categorias totais por quantidade (decrescente)
    sorted_total_categories = sorted(total_categories.items(), key=lambda x: x[1], reverse=True)
    
    month_label = f'{MONTHS_PT[month_num]} de {year}'
    
    return jsonify({
        'projects': projects_result,
        'total_categories': [{'name': cat, 'count': count} for cat, count in sorted_total_categories],
        'grand_total': grand_total,
        'month_label': month_label
    })
