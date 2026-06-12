"""
Modelos de dados do Hórus Operacional
"""
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    """Callback para Flask-Login carregar usuário"""
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    """Modelo de usuário com autenticação"""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='visualizador')  # admin, supervisor, visualizador
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def set_password(self, password):
        """Gerar hash da senha"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verificar senha"""
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        """Verificar se Ü admin"""
        return self.role == 'admin'
    
    def is_supervisor(self):
        """Verificar se Ü supervisor ou admin"""
        return self.role in ['admin', 'supervisor']
    
    def __repr__(self):
        return f'<User {self.email}>'


class Project(db.Model):
    """Modelo de projeto"""
    
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    status = db.Column(db.String(20), nullable=False, default='active')  # active, inactive
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    planning_weeks = db.relationship('PlanningWeek', backref='project', lazy=True, cascade='all, delete-orphan')
    professionals = db.relationship('Professional', backref='project', lazy=True)
    weekly_attendances = db.relationship('WeeklyAttendance', backref='project', lazy=True)
    holidays = db.relationship('Holiday', backref='project', lazy=True)
    
    def __repr__(self):
        return f'<Project {self.name}>'


class Professional(db.Model):
    """Modelo de profissional"""
    
    __tablename__ = 'professionals'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    registration = db.Column(db.String(50), unique=True, nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='active')  # active, inactive
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    weekly_attendances = db.relationship('WeeklyAttendance', backref='professional', lazy=True)
    
    def __repr__(self):
        return f'<Professional {self.name}>'


class PlanningWeek(db.Model):
    """Modelo de planejamento semanal"""
    
    __tablename__ = 'planning_weeks'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    week_label = db.Column(db.String(50), nullable=False)  # ex: "Semana 25"
    start_date = db.Column(db.Date, nullable=False)  # Segunda-feira
    end_date = db.Column(db.Date, nullable=False)  # Sexta-feira
    source_file_name = db.Column(db.String(200))  # Nome do arquivo importado (se houver)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    creator = db.relationship('User', foreign_keys=[created_by])
    weekly_attendances = db.relationship('WeeklyAttendance', backref='planning_week', lazy=True, cascade='all, delete-orphan')
    holidays = db.relationship('Holiday', backref='planning_week', lazy=True)
    
    def __repr__(self):
        return f'<PlanningWeek {self.week_label}>'


class WeeklyAttendance(db.Model):
    """Modelo de presença semanal"""
    
    __tablename__ = 'weekly_attendance'
    
    # Status possÜveis
    STATUS_PRESENTE = 'Presente'
    STATUS_FALTA_JUSTIFICADA = 'Falta justificada'
    STATUS_FALTA_NAO_JUSTIFICADA = 'Falta não justificada'
    STATUS_SAIDA_ANTECIPADA = 'SaÜda antecipada'
    STATUS_REALOCADO = 'Realocado'
    STATUS_FERIADO = 'Feriado'
    STATUS_FOLGA = 'Folga'
    STATUS_NAO_PLANEJADO = 'NÜo planejado'
    
    VALID_STATUSES = [
        STATUS_PRESENTE,
        STATUS_FALTA_JUSTIFICADA,
        STATUS_FALTA_NAO_JUSTIFICADA,
        STATUS_SAIDA_ANTECIPADA,
        STATUS_REALOCADO,
        STATUS_FERIADO,
        STATUS_FOLGA,
        STATUS_NAO_PLANEJADO
    ]
    
    id = db.Column(db.Integer, primary_key=True)
    planning_week_id = db.Column(db.Integer, db.ForeignKey('planning_weeks.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('professionals.id'), nullable=False)
    monday_status = db.Column(db.String(50), nullable=False, default=STATUS_PRESENTE)
    monday_activities = db.Column(db.Text)  # Atividades detalhadas da segunda
    tuesday_status = db.Column(db.String(50), nullable=False, default=STATUS_PRESENTE)
    tuesday_activities = db.Column(db.Text)  # Atividades detalhadas da terça
    wednesday_status = db.Column(db.String(50), nullable=False, default=STATUS_PRESENTE)
    wednesday_activities = db.Column(db.Text)  # Atividades detalhadas da quarta
    thursday_status = db.Column(db.String(50), nullable=False, default=STATUS_PRESENTE)
    thursday_activities = db.Column(db.Text)  # Atividades detalhadas da quinta
    friday_status = db.Column(db.String(50), nullable=False, default=STATUS_PRESENTE)
    friday_activities = db.Column(db.Text)  # Atividades detalhadas da sexta
    notes = db.Column(db.Text)
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    updater = db.relationship('User', foreign_keys=[updated_by])
    
    @staticmethod
    def is_valid_day(status):
        """Verifica se o status conta no denominador"""
        return status in [
            WeeklyAttendance.STATUS_PRESENTE,
            WeeklyAttendance.STATUS_FALTA_JUSTIFICADA,
            WeeklyAttendance.STATUS_FALTA_NAO_JUSTIFICADA,
            WeeklyAttendance.STATUS_SAIDA_ANTECIPADA,
            WeeklyAttendance.STATUS_REALOCADO
        ]
    
    @staticmethod
    def is_present(status):
        """Verifica se o status conta como presença"""
        return status in [
            WeeklyAttendance.STATUS_PRESENTE,
            WeeklyAttendance.STATUS_SAIDA_ANTECIPADA,
            WeeklyAttendance.STATUS_REALOCADO
        ]
    
    def get_week_statuses(self):
        """Retorna lista de status da semana"""
        return [
            self.monday_status,
            self.tuesday_status,
            self.wednesday_status,
            self.thursday_status,
            self.friday_status
        ]
    
    def calculate_metrics(self):
        """Calcula métricas de assiduidade"""
        statuses = self.get_week_statuses()
        
        valid_days = sum(1 for s in statuses if self.is_valid_day(s))
        present_days = sum(1 for s in statuses if self.is_present(s))
        
        rate = (present_days / valid_days * 100) if valid_days > 0 else None
        
        return {
            'valid_days': valid_days,
            'present_days': present_days,
            'rate': rate
        }
    
    def __repr__(self):
        return f'<WeeklyAttendance {self.professional.name}>'


class Holiday(db.Model):
    """Modelo de feriado"""
    
    __tablename__ = 'holidays'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    planning_week_id = db.Column(db.Integer, db.ForeignKey('planning_weeks.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    weekday = db.Column(db.String(20), nullable=False)  # Monday, Tuesday, etc
    description = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Holiday {self.date} - {self.description}>'


class AuditLog(db.Model):
    """Modelo de log de auditoria"""
    
    __tablename__ = 'audit_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    action = db.Column(db.String(50), nullable=False)  # login, create, update, delete, export, etc
    entity = db.Column(db.String(50), nullable=False)  # user, project, professional, planning, attendance, etc
    entity_id = db.Column(db.Integer)  # ID da entidade afetada
    details = db.Column(db.Text)  # JSON com detalhes da ação
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    user = db.relationship('User', foreign_keys=[user_id])
    
    def __repr__(self):
        return f'<AuditLog {self.action} {self.entity}>'
