"""
Rotas principais da aplica????o
"""
from flask import Blueprint, render_template, jsonify, redirect, url_for
from flask_login import login_required, current_user
from app.models import Project, Professional, PlanningWeek, User

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    """Página inicial - redireciona para login ou dashboard"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('auth.login'))


@bp.route('/dashboard')
@login_required
def dashboard():
    """Dashboard principal com estatísticas e atalhos"""
    # Calcular estatísticas
    stats = {
        'total_projects': Project.query.filter_by(status='active').count(),
        'active_professionals': Professional.query.filter_by(status='active').count(),
        'total_weeks': PlanningWeek.query.count(),
        'total_users': User.query.count()
    }
    
    return render_template('dashboard.html', stats=stats)


@bp.route('/health')
def health():
    """Health check para monitoramento"""
    return jsonify({
        'status': 'ok',
        'app': 'Hórus Operacional',
        'version': '2.0.0'
    })
