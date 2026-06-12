"""
Rotas do quadro semanal e funcionalidades principais
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, make_response
from flask_login import login_required, current_user
from datetime import datetime, date, timedelta
from app import db
from app.models import (Project, Professional, PlanningWeek, WeeklyAttendance, 
                       Holiday, AuditLog, User)
import json
import csv
from io import StringIO

bp = Blueprint('weekly', __name__, url_prefix='/weekly')


@bp.route('/')
@login_required
def index():
    """Quadro semanal principal"""
    projects = Project.query.filter_by(status='active').order_by(Project.name).all()
    weeks = PlanningWeek.query.order_by(PlanningWeek.start_date.desc()).limit(10).all()
    
    return render_template('weekly/index.html', projects=projects, weeks=weeks)


@bp.route('/api/weeks')
@login_required
def get_weeks():
    """API: Listar semanas por projeto"""
    project_id = request.args.get('project_id', type=int)
    
    if not project_id:
        return jsonify({'error': 'project_id required'}), 400
    
    weeks = PlanningWeek.query.filter_by(project_id=project_id)\
        .order_by(PlanningWeek.start_date.desc()).all()
    
    return jsonify([{
        'id': w.id,
        'label': w.week_label,
        'start_date': w.start_date.isoformat(),
        'end_date': w.end_date.isoformat()
    } for w in weeks])


@bp.route('/api/load')
@login_required
def load_board():
    """API: Carregar quadro semanal"""
    week_id = request.args.get('week_id', type=int)
    
    if not week_id:
        return jsonify({'error': 'week_id required'}), 400
    
    week = PlanningWeek.query.get_or_404(week_id)
    attendances = WeeklyAttendance.query.filter_by(planning_week_id=week_id).all()
    holidays = Holiday.query.filter_by(planning_week_id=week_id).all()
    
    # Calcular indicadores
    total_valid = 0
    total_present = 0
    total_falta_j = 0
    total_falta_nj = 0
    total_saida = 0
    total_realoc = 0
    total_feriados = 0
    
    attendance_data = []
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
        
        # Calcular assiduidade individual do profissional
        attendance_rate = (present_days / valid_days * 100) if valid_days > 0 else 0
        
        attendance_data.append({
            'id': att.id,
            'professional': {
                'id': att.professional.id,
                'name': att.professional.name,
                'registration': att.professional.registration
            },
            'monday': att.monday_status,
            'monday_activities': att.monday_activities or '',
            'tuesday': att.tuesday_status,
            'tuesday_activities': att.tuesday_activities or '',
            'wednesday': att.wednesday_status,
            'wednesday_activities': att.wednesday_activities or '',
            'thursday': att.thursday_status,
            'thursday_activities': att.thursday_activities or '',
            'friday': att.friday_status,
            'friday_activities': att.friday_activities or '',
            'notes': att.notes or '',
            'attendance_rate': round(attendance_rate, 1)
        })
    
    # Taxa de assiduidade m??dia (m??dia das taxas individuais)
    individual_rates = [att['attendance_rate'] for att in attendance_data if att['attendance_rate'] > 0]
    avg_rate = sum(individual_rates) / len(individual_rates) if individual_rates else None
    
    return jsonify({
        'week': {
            'id': week.id,
            'label': week.week_label,
            'start_date': week.start_date.isoformat(),
            'end_date': week.end_date.isoformat(),
            'project': week.project.name
        },
        'attendances': attendance_data,
        'holidays': [{
            'id': h.id,
            'date': h.date.isoformat(),
            'weekday': h.weekday,
            'description': h.description
        } for h in holidays],
        'metrics': {
            'rate': round(avg_rate, 2) if avg_rate else None,
            'professionals': len(attendances),
            'valid_days': total_valid,
            'present_days': total_present,
            'falta_justificada': total_falta_j,
            'falta_nao_justificada': total_falta_nj,
            'saida_antecipada': total_saida,
            'realocacoes': total_realoc,
            'feriados': total_feriados
        }
    })


@bp.route('/api/save', methods=['POST'])
@login_required
def save_board():
    """API: Salvar alterações do quadro"""
    if not current_user.is_supervisor():
        return jsonify({'error': 'Permiss??o negada'}), 403
    
    data = request.get_json()
    week_id = data.get('week_id')
    changes = data.get('changes', [])
    
    if not week_id:
        return jsonify({'error': 'week_id required'}), 400
    
    week = PlanningWeek.query.get_or_404(week_id)
    
    # Validar status
    valid_statuses = WeeklyAttendance.VALID_STATUSES
    
    for change in changes:
        att_id = change.get('id')
        attendance = WeeklyAttendance.query.get_or_404(att_id)
        
        # Atualizar status
        if 'monday' in change:
            if change['monday'] not in valid_statuses:
                return jsonify({'error': f'Status invêlido: {change["monday"]}'}), 400
            attendance.monday_status = change['monday']
        
        if 'tuesday' in change:
            if change['tuesday'] not in valid_statuses:
                return jsonify({'error': f'Status invêlido: {change["tuesday"]}'}), 400
            attendance.tuesday_status = change['tuesday']
        
        if 'wednesday' in change:
            if change['wednesday'] not in valid_statuses:
                return jsonify({'error': f'Status invêlido: {change["wednesday"]}'}), 400
            attendance.wednesday_status = change['wednesday']
        
        if 'thursday' in change:
            if change['thursday'] not in valid_statuses:
                return jsonify({'error': f'Status invêlido: {change["thursday"]}'}), 400
            attendance.thursday_status = change['thursday']
        
        if 'friday' in change:
            if change['friday'] not in valid_statuses:
                return jsonify({'error': f'Status invêlido: {change["friday"]}'}), 400
            attendance.friday_status = change['friday']
        
        if 'notes' in change:
            attendance.notes = change['notes']
        
        attendance.updated_by = current_user.id
    
    db.session.commit()
    
    # Log de auditoria
    log = AuditLog(
        user_id=current_user.id,
        action='update',
        entity='attendance',
        entity_id=week_id,
        details=json.dumps({
            'week': week.week_label,
            'changes_count': len(changes)
        })
    )
    db.session.add(log)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Alterações salvas com sucesso!'})


@bp.route('/api/generate', methods=['POST'])
@login_required
def generate_planning():
    """API: Gerar planejamento semanal"""
    if not current_user.is_supervisor():
        return jsonify({'error': 'Permiss??o negada'}), 403
    
    data = request.get_json()
    project_id = data.get('project_id')
    week_label = data.get('week_label')
    start_date_str = data.get('start_date')
    end_date_str = data.get('end_date')
    
    if not all([project_id, week_label, start_date_str, end_date_str]):
        return jsonify({'error': 'Dados incompletos'}), 400
    
    project = Project.query.get_or_404(project_id)
    
    # Converter datas
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    
    # Validar: segunda a sexta
    if start_date.weekday() != 0 or end_date.weekday() != 4:
        return jsonify({'error': 'Deve ser segunda a sexta-feira'}), 400
    
    # Verificar se j?? existe
    existing = PlanningWeek.query.filter_by(
        project_id=project_id,
        start_date=start_date
    ).first()
    
    if existing:
        return jsonify({'error': 'Planejamento j?? existe para esta semana'}), 400
    
    # Criar planejamento
    week = PlanningWeek(
        project_id=project_id,
        week_label=week_label,
        start_date=start_date,
        end_date=end_date,
        created_by=current_user.id
    )
    db.session.add(week)
    db.session.flush()
    
    # Criar registros de presença para todos os profissionais ativos do projeto
    professionals = Professional.query.filter_by(
        project_id=project_id,
        status='active'
    ).all()
    
    for prof in professionals:
        attendance = WeeklyAttendance(
            planning_week_id=week.id,
            project_id=project_id,
            professional_id=prof.id,
            monday_status='Presente',
            tuesday_status='Presente',
            wednesday_status='Presente',
            thursday_status='Presente',
            friday_status='Presente',
            updated_by=current_user.id
        )
        db.session.add(attendance)
    
    db.session.commit()
    
    # Log
    log = AuditLog(
        user_id=current_user.id,
        action='create',
        entity='planning',
        entity_id=week.id,
        details=json.dumps({
            'project': project.name,
            'week': week_label,
            'professionals': len(professionals)
        })
    )
    db.session.add(log)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': f'Planejamento criado com {len(professionals)} profissionais!',
        'week_id': week.id
    })


@bp.route('/api/holiday/apply', methods=['POST'])
@login_required
def apply_holiday():
    """API: Aplicar feriado em um dia da semana"""
    if not current_user.is_supervisor():
        return jsonify({'error': 'Permiss??o negada'}), 403
    
    data = request.get_json()
    week_id = data.get('week_id')
    weekday = data.get('weekday')  # Monday, Tuesday, etc
    description = data.get('description')
    
    if not all([week_id, weekday, description]):
        return jsonify({'error': 'Dados incompletos'}), 400
    
    week = PlanningWeek.query.get_or_404(week_id)
    
    # Mapear dia da semana para coluna
    weekday_map = {
        'Monday': ('monday_status', 0),
        'Tuesday': ('tuesday_status', 1),
        'Wednesday': ('wednesday_status', 2),
        'Thursday': ('thursday_status', 3),
        'Friday': ('friday_status', 4)
    }
    
    if weekday not in weekday_map:
        return jsonify({'error': 'Dia invêlido'}), 400
    
    column, offset = weekday_map[weekday]
    holiday_date = week.start_date + timedelta(days=offset)
    
    # Verificar se j?? existe
    existing = Holiday.query.filter_by(
        planning_week_id=week_id,
        date=holiday_date
    ).first()
    
    if existing:
        return jsonify({'error': 'Feriado j?? aplicado neste dia'}), 400
    
    # Criar feriado
    holiday = Holiday(
        project_id=week.project_id,
        planning_week_id=week_id,
        date=holiday_date,
        weekday=weekday,
        description=description
    )
    db.session.add(holiday)
    
    # Atualizar todos os registros de presença para "Feriado"
    attendances = WeeklyAttendance.query.filter_by(planning_week_id=week_id).all()
    for att in attendances:
        setattr(att, column, 'Feriado')
        att.updated_by = current_user.id
    
    db.session.commit()
    
    # Log
    log = AuditLog(
        user_id=current_user.id,
        action='apply_holiday',
        entity='holiday',
        entity_id=holiday.id,
        details=json.dumps({
            'week': week.week_label,
            'date': holiday_date.isoformat(),
            'description': description
        })
    )
    db.session.add(log)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': f'Feriado aplicado em {weekday}!',
        'holiday_id': holiday.id
    })


@bp.route('/api/holiday/remove', methods=['POST'])
@login_required
def remove_holiday():
    """API: Remover feriado"""
    if not current_user.is_supervisor():
        return jsonify({'error': 'Permiss??o negada'}), 403
    
    data = request.get_json()
    holiday_id = data.get('holiday_id')
    
    if not holiday_id:
        return jsonify({'error': 'holiday_id required'}), 400
    
    holiday = Holiday.query.get_or_404(holiday_id)
    week = holiday.planning_week
    
    # Mapear dia da semana para coluna
    weekday_map = {
        'Monday': 'monday_status',
        'Tuesday': 'tuesday_status',
        'Wednesday': 'wednesday_status',
        'Thursday': 'thursday_status',
        'Friday': 'friday_status'
    }
    
    column = weekday_map.get(holiday.weekday)
    
    # Restaurar para "Presente"
    attendances = WeeklyAttendance.query.filter_by(planning_week_id=week.id).all()
    for att in attendances:
        if getattr(att, column) == 'Feriado':
            setattr(att, column, 'Presente')
            att.updated_by = current_user.id
    
    # Deletar feriado
    db.session.delete(holiday)
    db.session.commit()
    
    # Log
    log = AuditLog(
        user_id=current_user.id,
        action='remove_holiday',
        entity='holiday',
        entity_id=holiday_id,
        details=json.dumps({
            'week': week.week_label,
            'date': holiday.date.isoformat()
        })
    )
    db.session.add(log)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Feriado removido!'})


@bp.route('/export/csv')
@login_required
def export_csv():
    """Exportar quadro para CSV"""
    week_id = request.args.get('week_id', type=int)
    
    if not week_id:
        flash('Semana n??o especificada.', 'danger')
        return redirect(url_for('weekly.index'))
    
    week = PlanningWeek.query.get_or_404(week_id)
    attendances = WeeklyAttendance.query.filter_by(planning_week_id=week_id).all()
    
    # Criar CSV
    output = StringIO()
    writer = csv.writer(output)
    
    # Cabe??alho
    writer.writerow([
        'Profissional',
        'Matrícula',
        f'Segunda ({week.start_date.strftime("%d/%m")})',
        f'Ter??a ({(week.start_date + timedelta(days=1)).strftime("%d/%m")})',
        f'Quarta ({(week.start_date + timedelta(days=2)).strftime("%d/%m")})',
        f'Quinta ({(week.start_date + timedelta(days=3)).strftime("%d/%m")})',
        f'Sexta ({week.end_date.strftime("%d/%m")})',
        'Observações',
        'Dias V??lidos',
        'Dias Presentes',
        'Taxa (%)'
    ])
    
    # Dados
    for att in attendances:
        metrics = att.calculate_metrics()
        rate = metrics['rate']
        rate_str = f'{rate:.2f}%' if rate else 'N/A'
        
        writer.writerow([
            att.professional.name,
            att.professional.registration,
            att.monday_status,
            att.tuesday_status,
            att.wednesday_status,
            att.thursday_status,
            att.friday_status,
            att.notes or '',
            metrics['valid_days'],
            metrics['present_days'],
            rate_str
        ])
    
    # Log
    log = AuditLog(
        user_id=current_user.id,
        action='export',
        entity='attendance',
        entity_id=week_id,
        details=json.dumps({'week': week.week_label, 'format': 'csv'})
    )
    db.session.add(log)
    db.session.commit()
    
    # Retornar CSV
    output.seek(0)
    response = make_response(output.getvalue())
    response.headers['Content-Type'] = 'text/csv; charset=utf-8'
    response.headers['Content-Disposition'] = f'attachment; filename=horus_{week.week_label}_{week.start_date}.csv'
    
    return response
