"""
Rotas de importação de planejamento em PDF
"""
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
import re
import json
from datetime import datetime, timedelta
from app import db
from app.models import Project, Professional, PlanningWeek, WeeklyAttendance, Holiday, AuditLog
from app.ai_parser import PlanningAIParser  # Parser V2.0 Ultra-Robusto

bp = Blueprint('imports', __name__, url_prefix='/imports')

UPLOAD_FOLDER = 'temp_uploads'
ALLOWED_EXTENSIONS = {'pdf'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def allowed_file(filename):
    """Verifica se o arquivo ?? PDF"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def detect_holiday_in_activities(activities):
    """Detecta se as atividades indicam feriado/ponto facultativo"""
    if not activities:
        return False
    
    activities_lower = activities.lower()
    holiday_keywords = [
        'feriado',
        'ponto facultativo',
        'folga',
        'dia n??o letivo',
        'recesso',
        'emenda',
        'n??o haver?? expediente',
        'sem expediente',
        'dispensado'
    ]
    
    return any(keyword in activities_lower for keyword in holiday_keywords)

def count_activities(activities):
    """Conta quantas atividades existem em um texto"""
    if not activities:
        return 0
    acts = [a.strip() for a in activities.split('\n') if a.strip()]
    return len(acts)

def admin_or_supervisor_required(f):
    """Decorator para rotas que exigem admin ou supervisor"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        if current_user.role not in ['admin', 'supervisor']:
            flash('Voc?? n??o tem permiss??o para acessar esta página.', 'danger')
            return redirect(url_for('weekly.index'))
        return f(*args, **kwargs)
    return decorated_function


@bp.route('/')
@login_required
@admin_or_supervisor_required
def index():
    """Tela de importação de planejamento"""
    projects = Project.query.filter_by(status='active').order_by(Project.name).all()
    return render_template('imports/index.html', projects=projects)


@bp.route('/upload', methods=['POST'])
@login_required
@admin_or_supervisor_required
def upload():
    """Processa upload do PDF e retorna prévia"""
    try:
        # Validar arquivo primeiro
        if 'file' not in request.files:
            return jsonify({'error': 'Nenhum arquivo enviado'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Apenas arquivos PDF são permitidos'}), 400
        
        # Criar pasta temporária se não existir
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        
        # Salvar arquivo temporariamente
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        temp_filename = f"{timestamp}_{filename}"
        filepath = os.path.join(UPLOAD_FOLDER, temp_filename)
        file.save(filepath)
        
        # Usar agente de IA para parsing inicial (extrair nome do projeto)
        ai_parser = PlanningAIParser(filepath)
        initial_parse = ai_parser.parse_full_planning([])
        project_name_from_pdf = initial_parse.get('project_name', 'Projeto Sem Nome')
        
        # Verificar se foi fornecido project_id manualmente
        project_id = request.form.get('project_id', type=int)
        
        if project_id:
            # Usar projeto fornecido manualmente
            project = Project.query.get_or_404(project_id)
        else:
            # Buscar projeto pelo nome extraído do PDF
            project = Project.query.filter(
                Project.name.ilike(f"%{project_name_from_pdf}%")
            ).filter_by(status='active').first()
            
            if not project:
                # Criar novo projeto automaticamente
                project = Project(
                    name=project_name_from_pdf,
                    status='active'
                )
                db.session.add(project)
                db.session.flush()  # Para obter o ID sem commit
                
                # Registrar log de criação do projeto
                log_create = AuditLog(
                    user_id=current_user.id,
                    action='create_project_auto',
                    entity='project',
                    entity_id=project.id,
                    details=json.dumps({
                        'project_name': project_name_from_pdf,
                        'source': 'pdf_import',
                        'filename': filename
                    })
                )
                db.session.add(log_create)
        
        # Atualizar project_id para usar no restante do código
        project_id = project.id
        
        # Registrar log de upload
        log = AuditLog(
            user_id=current_user.id,
            action='upload_pdf',
            entity='import',
            entity_id=project_id,
            details=json.dumps({
                'filename': filename,
                'project': project.name,
                'extracted_project_name': project_name_from_pdf
            })
        )
        db.session.add(log)
        db.session.commit()
        
        # Buscar profissionais cadastrados do projeto
        registered_professionals = Professional.query.filter_by(
            project_id=project_id,
            status='active'
        ).all()
        
        # Usar agente de IA para parsing inteligente
        ai_parser = PlanningAIParser(filepath)
        parsed_data = ai_parser.parse_full_planning(registered_professionals)
        
        # Separar profissionais cadastrados vs n??o cadastrados
        registered_names = {p.name.lower().strip() for p in registered_professionals}
        registered_regs = {p.registration.strip() for p in registered_professionals}
        
        professionals_in_system = []
        professionals_not_in_system = []
        
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
        
        for prof in parsed_data['professionals']:
            prof_name = prof['name'].lower().strip()
            prof_reg = prof['registration'].strip()
            
            # Adicionar contadores e status sugeridos por dia
            for day in days:
                activities_key = f'{day}_activities'
                activities = prof.get(activities_key, '')
                
                # Contar atividades
                prof[f'{day}_count'] = count_activities(activities)
                
                # Detectar feriado e sugerir status
                if detect_holiday_in_activities(activities):
                    prof[f'{day}_status'] = 'feriado'
                else:
                    prof[f'{day}_status'] = 'presente'
            
            # Buscar profissional no banco por nome ou matrícula
            db_prof = Professional.query.filter_by(
                project_id=project_id,
                status='active'
            ).filter(
                (Professional.name.ilike(f"%{prof['name']}%")) |
                (Professional.registration == prof_reg)
            ).first()
            
            if db_prof:
                prof['id'] = db_prof.id
                prof['registered'] = True
                professionals_in_system.append(prof)
            else:
                prof['registered'] = False
                professionals_not_in_system.append(prof)
        
        # Extrair informações da semana
        week_info = parsed_data['week_info']
        
        # Se n??o identificou semana, tentar pegar do nome do arquivo
        if not week_info['week_label']:
            week_match = re.search(r'semana[_\s]*(\d+)', filename, re.IGNORECASE)
            if week_match:
                week_info['week_label'] = f"Semana {week_match.group(1)}"
        
        # Calcular datas
        start_date = None
        end_date = None
        
        if week_info['dates']:
            start_date = week_info['dates'][0].strftime('%Y-%m-%d')
            end_date = (week_info['dates'][0] + timedelta(days=4)).strftime('%Y-%m-%d')
        
        # Montar resultado da prévia
        preview_data = {
            'week_label': week_info['week_label'],
            'start_date': start_date,
            'end_date': end_date,
            'professionals': professionals_in_system,
            'unregistered': professionals_not_in_system,
            'alerts': parsed_data['alerts']
        }
        
        # Adicionar alerta se houver profissionais n??o cadastrados
        if professionals_not_in_system:
            preview_data['alerts'].insert(0, 
                f"{len(professionals_not_in_system)} profissional(is) n??o cadastrado(s) no sistema")
        
        # Armazenar dados na sess??o para confirmar depois
        session['import_data'] = {
            'project_id': project_id,
            'project_name': project.name,
            'filename': filename,
            'temp_filepath': filepath,
            'parsed_data': preview_data
        }
        
        # Retornar prévia
        return jsonify({
            'success': True,
            'preview': preview_data
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/confirm', methods=['POST'])
@login_required
@admin_or_supervisor_required
def confirm():
    """Confirma importação e gera quadro semanal"""
    try:
        # Recuperar dados da sess??o
        import_data = session.get('import_data')
        if not import_data:
            return jsonify({'error': 'Dados de importação n??o encontrados'}), 400
        
        # Recuperar dados do formul??rio (prévia editada)
        week_label = request.json.get('week_label')
        start_date = request.json.get('start_date')
        end_date = request.json.get('end_date')
        professionals_data = request.json.get('professionals', [])
        overwrite = request.json.get('overwrite', False)  # Nova op????o
        
        if not week_label or not start_date or not end_date:
            return jsonify({'error': 'Preencha todos os campos obrigat??rios'}), 400
        
        project_id = import_data['project_id']
        
        # Verificar se j?? existe planejamento para esta semana e projeto
        existing_week = PlanningWeek.query.filter_by(
            project_id=project_id,
            week_label=week_label
        ).first()
        
        if existing_week:
            if not overwrite:
                return jsonify({
                    'error': f'J?? existe planejamento "{week_label}" para este projeto',
                    'existing_week_id': existing_week.id,
                    'can_overwrite': True
                }), 409  # Conflict status code
            else:
                # Remover semana existente e seus relacionamentos
                Holiday.query.filter_by(planning_week_id=existing_week.id).delete()
                WeeklyAttendance.query.filter_by(planning_week_id=existing_week.id).delete()
                db.session.delete(existing_week)
                db.session.flush()
        
        # Criar PlanningWeek
        planning_week = PlanningWeek(
            project_id=project_id,
            week_label=week_label,
            start_date=datetime.strptime(start_date, '%Y-%m-%d').date(),
            end_date=datetime.strptime(end_date, '%Y-%m-%d').date(),
            created_by=current_user.id
        )
        db.session.add(planning_week)
        db.session.flush()  # Para obter o ID
        
        # Criar WeeklyAttendance para cada profissional
        for prof_data in professionals_data:
            attendance = WeeklyAttendance(
                project_id=project_id,
                professional_id=prof_data['id'],
                planning_week_id=planning_week.id,
                monday_status=prof_data.get('monday', 'Presente'),
                monday_activities=prof_data.get('monday_activities', ''),
                tuesday_status=prof_data.get('tuesday', 'Presente'),
                tuesday_activities=prof_data.get('tuesday_activities', ''),
                wednesday_status=prof_data.get('wednesday', 'Presente'),
                wednesday_activities=prof_data.get('wednesday_activities', ''),
                thursday_status=prof_data.get('thursday', 'Presente'),
                thursday_activities=prof_data.get('thursday_activities', ''),
                friday_status=prof_data.get('friday', 'Presente'),
                friday_activities=prof_data.get('friday_activities', '')
            )
            db.session.add(attendance)
        
        # Registrar log
        log = AuditLog(
            user_id=current_user.id,
            action='confirm_import',
            entity='planning_week',
            entity_id=planning_week.id,
            details=json.dumps({
                'project_id': project_id,
                'week_label': week_label,
                'filename': import_data['filename'],
                'professionals_count': len(professionals_data)
            })
        )
        db.session.add(log)
        
        db.session.commit()
        
        # Limpar arquivo tempor??rio
        try:
            if os.path.exists(import_data['temp_filepath']):
                os.remove(import_data['temp_filepath'])
        except:
            pass
        
        # Limpar dados da sess??o
        session.pop('import_data', None)
        
        return jsonify({
            'success': True,
            'message': f'Planejamento {week_label} importado com sucesso!',
            'week_id': planning_week.id
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/cancel', methods=['POST'])
@login_required
@admin_or_supervisor_required
def cancel():
    """Cancela importação e limpa arquivo tempor??rio"""
    try:
        import_data = session.get('import_data')
        if import_data:
            # Remover arquivo tempor??rio
            try:
                if os.path.exists(import_data['temp_filepath']):
                    os.remove(import_data['temp_filepath'])
            except:
                pass
            
            # Registrar log
            log = AuditLog(
                user_id=current_user.id,
                action='cancel_import',
                entity='import',
                entity_id=import_data['project_id'],
                details=json.dumps({'filename': import_data['filename']})
            )
            db.session.add(log)
            db.session.commit()
            
            # Limpar sess??o
            session.pop('import_data', None)
        
        return jsonify({'success': True})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/quick-register', methods=['POST'])
@login_required
@admin_or_supervisor_required
def quick_register():
    """Cadastro r??pido de profissionais n??o cadastrados"""
    try:
        data = request.json
        professionals_data = data.get('professionals', [])
        
        if not professionals_data:
            return jsonify({'error': 'Nenhum profissional para cadastrar'}), 400
        
        registered_count = 0
        
        for prof_data in professionals_data:
            name = prof_data.get('name', '').strip()
            registration = prof_data.get('registration', '').strip()
            project_id = prof_data.get('project_id')
            
            if not name or not registration or not project_id:
                continue
            
            # Verificar se j?? existe
            existing = Professional.query.filter_by(
                registration=registration,
                project_id=project_id
            ).first()
            
            if existing:
                continue
            
            # Criar novo profissional
            professional = Professional(
                name=name,
                registration=registration,
                project_id=project_id,
                status='active',
                created_by=current_user.id
            )
            db.session.add(professional)
            registered_count += 1
            
            # Log
            log = AuditLog(
                user_id=current_user.id,
                action='quick_register',
                entity='professional',
                entity_id=None,
                details=json.dumps({
                    'name': name,
                    'registration': registration,
                    'project_id': project_id,
                    'from': 'import_flow'
                })
            )
            db.session.add(log)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'registered_count': registered_count
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/create-project', methods=['POST'])
@login_required
@admin_or_supervisor_required
def create_project():
    """Cria????o r??pida de projeto durante importação"""
    try:
        data = request.json
        project_name = data.get('name', '').strip()
        
        if not project_name:
            return jsonify({'error': 'Nome do projeto ?? obrigat??rio'}), 400
        
        # Verificar se j?? existe
        existing = Project.query.filter_by(name=project_name).first()
        if existing:
            return jsonify({'error': f'Projeto "{project_name}" j?? existe'}), 400
        
        # Criar novo projeto
        project = Project(
            name=project_name,
            status='active',
            created_by=current_user.id
        )
        db.session.add(project)
        db.session.flush()
        
        # Log
        log = AuditLog(
            user_id=current_user.id,
            action='quick_create',
            entity='project',
            entity_id=project.id,
            details=json.dumps({
                'name': project_name,
                'from': 'import_flow'
            })
        )
        db.session.add(log)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'project_id': project.id,
            'project_name': project.name
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
