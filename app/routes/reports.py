"""
Rotas de indicadores e relat??rios
"""
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from datetime import datetime, date
from app import db
from app.models import Project, Professional, PlanningWeek, WeeklyAttendance
from sqlalchemy import and_

bp = Blueprint('reports', __name__, url_prefix='/reports')


@bp.route('/')
@login_required
def index():
    """Tela de indicadores"""
    projects = Project.query.filter_by(status='active').order_by(Project.name).all()
    professionals = Professional.query.filter_by(status='active').order_by(Professional.name).all()
    
    return render_template('reports/index.html', projects=projects, professionals=professionals)


@bp.route('/api/metrics')
@login_required
def get_metrics():
    """API: Obter indicadores com filtros"""
    # Filtros
    project_id = request.args.get('project_id', type=int)
    professional_id = request.args.get('professional_id', type=int)
    week_id = request.args.get('week_id', type=int)
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    
    # Query base
    query = WeeklyAttendance.query.join(PlanningWeek)
    
    # Aplicar filtros
    if project_id:
        query = query.filter(WeeklyAttendance.project_id == project_id)
    
    if professional_id:
        query = query.filter(WeeklyAttendance.professional_id == professional_id)
    
    if week_id:
        query = query.filter(WeeklyAttendance.planning_week_id == week_id)
    
    if start_date_str and end_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        query = query.filter(
            and_(
                PlanningWeek.start_date >= start_date,
                PlanningWeek.end_date <= end_date
            )
        )
    
    attendances = query.all()
    
    # Calcular m??tricas agregadas
    total_valid = 0
    total_present = 0
    total_falta_j = 0
    total_falta_nj = 0
    total_saida = 0
    total_realoc = 0
    total_feriados = 0
    
    professional_metrics = {}
    
    for att in attendances:
        statuses = att.get_week_statuses()
        
        valid_days = sum(1 for s in statuses if WeeklyAttendance.is_valid_day(s))
        present_days = sum(1 for s in statuses if WeeklyAttendance.is_present(s))
        
        total_valid += valid_days
        total_present += present_days
        total_falta_j += statuses.count('Falta justificada')
        total_falta_nj += statuses.count('Falta n??o justificada')
        total_saida += statuses.count('Sa??da antecipada')
        total_realoc += statuses.count('Realocado')
        total_feriados += statuses.count('Feriado')
        
        # M??tricas por profissional
        prof_id = att.professional_id
        if prof_id not in professional_metrics:
            professional_metrics[prof_id] = {
                'name': att.professional.name,
                'registration': att.professional.registration,
                'valid_days': 0,
                'present_days': 0,
                'falta_j': 0,
                'falta_nj': 0
            }
        
        professional_metrics[prof_id]['valid_days'] += valid_days
        professional_metrics[prof_id]['present_days'] += present_days
        professional_metrics[prof_id]['falta_j'] += statuses.count('Falta justificada')
        professional_metrics[prof_id]['falta_nj'] += statuses.count('Falta n??o justificada')
    
    # Calcular taxas
    global_rate = (total_present / total_valid * 100) if total_valid > 0 else None
    
    for prof_id, metrics in professional_metrics.items():
        vd = metrics['valid_days']
        pd = metrics['present_days']
        metrics['rate'] = (pd / vd * 100) if vd > 0 else None
    
    return jsonify({
        'global': {
            'total_valid': total_valid,
            'total_present': total_present,
            'rate': round(global_rate, 2) if global_rate else None,
            'falta_justificada': total_falta_j,
            'falta_nao_justificada': total_falta_nj,
            'saida_antecipada': total_saida,
            'realocacoes': total_realoc,
            'feriados': total_feriados
        },
        'by_professional': list(professional_metrics.values())
    })
