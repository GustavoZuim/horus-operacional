"""
Rotas de CRUD de usu??rios (Admin only)
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from functools import wraps
from app import db
from app.models import User, AuditLog
import json

bp = Blueprint('users', __name__, url_prefix='/users')


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
    """Lista todos os usu??rios"""
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('users/index.html', users=users)


@bp.route('/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create():
    """Criar novo usu??rio"""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role', 'visualizador')
        
        # Valida????es
        if not name or not email or not password:
            flash('Todos os campos s??o obrigat??rios.', 'danger')
            return render_template('users/form.html')
        
        # Verificar se email j?? existe
        existing = User.query.filter_by(email=email).first()
        if existing:
            flash('Email j?? cadastrado.', 'danger')
            return render_template('users/form.html')
        
        # Criar usu??rio
        user = User(
            name=name,
            email=email,
            role=role,
            active=True
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        # Log de auditoria
        log = AuditLog(
            user_id=current_user.id,
            action='create',
            entity='user',
            entity_id=user.id,
            details=json.dumps({'name': name, 'email': email, 'role': role})
        )
        db.session.add(log)
        db.session.commit()
        
        flash(f'Usu??rio {name} criado com sucesso!', 'success')
        return redirect(url_for('users.index'))
    
    return render_template('users/form.html')


@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit(id):
    """Editar usu??rio"""
    user = User.query.get_or_404(id)
    
    if request.method == 'POST':
        user.name = request.form.get('name')
        user.email = request.form.get('email')
        user.role = request.form.get('role')
        user.active = request.form.get('active') == 'on'
        
        # Atualizar senha se fornecida
        password = request.form.get('password')
        if password:
            user.set_password(password)
        
        db.session.commit()
        
        # Log de auditoria
        log = AuditLog(
            user_id=current_user.id,
            action='update',
            entity='user',
            entity_id=user.id,
            details=json.dumps({'name': user.name, 'email': user.email, 'role': user.role})
        )
        db.session.add(log)
        db.session.commit()
        
        flash(f'Usu??rio {user.name} atualizado!', 'success')
        return redirect(url_for('users.index'))
    
    return render_template('users/form.html', user=user)


@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete(id):
    """Desativar usu??rio"""
    user = User.query.get_or_404(id)
    
    # N??o permitir desativar a si mesmo
    if user.id == current_user.id:
        flash('Voc?? n??o pode desativar seu pr??prio usu??rio.', 'danger')
        return redirect(url_for('users.index'))
    
    user.active = False
    db.session.commit()
    
    # Log de auditoria
    log = AuditLog(
        user_id=current_user.id,
        action='delete',
        entity='user',
        entity_id=user.id,
        details=json.dumps({'name': user.name, 'email': user.email})
    )
    db.session.add(log)
    db.session.commit()
    
    flash(f'Usu??rio {user.name} desativado.', 'warning')
    return redirect(url_for('users.index'))
