"""
Rotas de CRUD de projetos (Admin only)
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from functools import wraps
from app import db
from app.models import Project, AuditLog
import json

bp = Blueprint('projects', __name__, url_prefix='/projects')


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
    """Lista todos os projetos"""
    projects = Project.query.order_by(Project.name).all()
    return render_template('projects/index.html', projects=projects)


@bp.route('/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create():
    """Criar novo projeto"""
    if request.method == 'POST':
        name = request.form.get('name')
        
        if not name:
            flash('Nome do projeto ?? obrigat??rio.', 'danger')
            return render_template('projects/form.html')
        
        # Verificar se j?? existe
        existing = Project.query.filter_by(name=name).first()
        if existing:
            flash('Projeto j?? cadastrado.', 'danger')
            return render_template('projects/form.html')
        
        project = Project(name=name, status='active')
        db.session.add(project)
        db.session.commit()
        
        # Log
        log = AuditLog(
            user_id=current_user.id,
            action='create',
            entity='project',
            entity_id=project.id,
            details=json.dumps({'name': name})
        )
        db.session.add(log)
        db.session.commit()
        
        flash(f'Projeto {name} criado com sucesso!', 'success')
        return redirect(url_for('projects.index'))
    
    return render_template('projects/form.html')


@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit(id):
    """Editar projeto"""
    project = Project.query.get_or_404(id)
    
    if request.method == 'POST':
        project.name = request.form.get('name')
        project.status = request.form.get('status', 'active')
        
        db.session.commit()
        
        # Log
        log = AuditLog(
            user_id=current_user.id,
            action='update',
            entity='project',
            entity_id=project.id,
            details=json.dumps({'name': project.name, 'status': project.status})
        )
        db.session.add(log)
        db.session.commit()
        
        flash(f'Projeto {project.name} atualizado!', 'success')
        return redirect(url_for('projects.index'))
    
    return render_template('projects/form.html', project=project)


@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete(id):
    """Inativar projeto"""
    project = Project.query.get_or_404(id)
    project.status = 'inactive'
    db.session.commit()
    
    # Log
    log = AuditLog(
        user_id=current_user.id,
        action='delete',
        entity='project',
        entity_id=project.id,
        details=json.dumps({'name': project.name})
    )
    db.session.add(log)
    db.session.commit()
    
    flash(f'Projeto {project.name} inativado.', 'warning')
    return redirect(url_for('projects.index'))
