"""
Rotas de autenticação
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User, AuditLog
import json

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember', False)
        
        user = User.query.filter_by(email=email, active=True).first()
        
        if user and user.check_password(password):
            login_user(user, remember=remember)
            
            # Log de login
            log = AuditLog(
                user_id=user.id,
                action='login',
                entity='session',
                entity_id=user.id,
                details=json.dumps({'email': email})
            )
            db.session.add(log)
            db.session.commit()
            
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.dashboard'))
        else:
            flash('Email ou senha incorretos.', 'danger')
    
    return render_template('auth/login.html')


@bp.route('/logout')
@login_required
def logout():
    """Logout"""
    # Log de logout
    log = AuditLog(
        user_id=current_user.id,
        action='logout',
        entity='session',
        entity_id=current_user.id,
        details=json.dumps({'user': current_user.name})
    )
    db.session.add(log)
    db.session.commit()
    
    logout_user()
    flash('Você saiu com sucesso.', 'success')
    return redirect(url_for('auth.login'))
