"""
Rotas de logs de auditoria
"""
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app.models import AuditLog, User
from functools import wraps

bp = Blueprint('logs', __name__, url_prefix='/logs')


def admin_required(f):
    """Decorator para rotas que exigem admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            return jsonify({'error': 'Acesso negado'}), 403
        return f(*args, **kwargs)
    return decorated_function


@bp.route('/')
@login_required
@admin_required
def index():
    """Tela de logs"""
    users = User.query.filter_by(active=True).order_by(User.name).all()
    return render_template('logs/index.html', users=users)


@bp.route('/api/list')
@login_required
@admin_required
def list_logs():
    """API: Listar logs com filtros"""
    # Filtros
    user_id = request.args.get('user_id', type=int)
    action = request.args.get('action')
    entity = request.args.get('entity')
    limit = request.args.get('limit', 100, type=int)
    
    # Query
    query = AuditLog.query
    
    if user_id:
        query = query.filter_by(user_id=user_id)
    
    if action:
        query = query.filter_by(action=action)
    
    if entity:
        query = query.filter_by(entity=entity)
    
    logs = query.order_by(AuditLog.created_at.desc()).limit(limit).all()
    
    return jsonify([{
        'id': log.id,
        'user': log.user.name,
        'action': log.action,
        'entity': log.entity,
        'entity_id': log.entity_id,
        'details': log.details,
        'created_at': log.created_at.isoformat()
    } for log in logs])
