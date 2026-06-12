"""
Rotas de CRUD de profissionais (Admin only)
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from functools import wraps
from app import db
from app.models import Professional, Project, AuditLog
import json

bp = Blueprint('professionals', __name__, url_prefix='/professionals')


def admin_required(f):
    """Decorator para rotas que exigem admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('Acesso negado. Apenas administradores.', 'danger')
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    return decorated_function


@bp.route('/')
@login_required
@admin_required
def index():
    """Lista todos os profissionais"""
    professionals = Professional.query.order_by(Professional.name).all()
    return render_template('professionals/index.html', professionals=professionals)


@bp.route('/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create():
    """Criar novo profissional"""
    projects = Project.query.filter_by(status='active').all()
    
    if request.method == 'POST':
        name = request.form.get('name')
        registration = request.form.get('registration')
        project_id = request.form.get('project_id')
        
        if not name or not registration or not project_id:
            flash('Todos os campos s??o obrigat??rios.', 'danger')
            return render_template('professionals/form.html', projects=projects)
        
        # Verificar se matrícula j?? existe
        existing = Professional.query.filter_by(registration=registration).first()
        if existing:
            flash('Matrícula j?? cadastrada.', 'danger')
            return render_template('professionals/form.html', projects=projects)
        
        professional = Professional(
            name=name,
            registration=registration,
            project_id=int(project_id),
            status='active'
        )
        db.session.add(professional)
        db.session.commit()
        
        # Log
        log = AuditLog(
            user_id=current_user.id,
            action='create',
            entity='professional',
            entity_id=professional.id,
            details=json.dumps({'name': name, 'registration': registration})
        )
        db.session.add(log)
        db.session.commit()
        
        flash(f'Profissional {name} criado com sucesso!', 'success')
        return redirect(url_for('professionals.index'))
    
    return render_template('professionals/form.html', projects=projects)


@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit(id):
    """Editar profissional"""
    professional = Professional.query.get_or_404(id)
    projects = Project.query.filter_by(status='active').all()
    
    if request.method == 'POST':
        professional.name = request.form.get('name')
        professional.registration = request.form.get('registration')
        professional.project_id = int(request.form.get('project_id'))
        professional.status = request.form.get('status', 'active')
        
        db.session.commit()
        
        # Log
        log = AuditLog(
            user_id=current_user.id,
            action='update',
            entity='professional',
            entity_id=professional.id,
            details=json.dumps({'name': professional.name, 'registration': professional.registration})
        )
        db.session.add(log)
        db.session.commit()
        
        flash(f'Profissional {professional.name} atualizado!', 'success')
        return redirect(url_for('professionals.index'))
    
    return render_template('professionals/form.html', professional=professional, projects=projects)


@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete(id):
    """Inativar profissional"""
    professional = Professional.query.get_or_404(id)
    professional.status = 'inactive'
    db.session.commit()
    
    # Log
    log = AuditLog(
        user_id=current_user.id,
        action='delete',
        entity='professional',
        entity_id=professional.id,
        details=json.dumps({'name': professional.name})
    )
    db.session.add(log)
    db.session.commit()
    
    flash(f'Profissional {professional.name} inativado.', 'warning')
    return redirect(url_for('professionals.index'))
