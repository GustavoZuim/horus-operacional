# ???? Guia de Deploy - H??rus Operacional

## ??? Quick Start (Desenvolvimento)

```bash
# 1. Clone e entre no diret??rio
cd horus-operacional

# 2. Crie o ambiente virtual
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 3. Instale depend??ncias
pip install -r requirements.txt

# 4. Inicialize o banco de dados
python init_db.py

# 5. Execute
python run.py
```

**Credenciais padr??o:**
- Email: `admin@horus.local`
- Senha: `admin123`

?????? **Altere a senha ap??s o primeiro login!**

---

## ???? Deploy em Produ????o

### Op????o 1: VPS/Servidor Linux

#### 1. Preparar o Servidor

```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Python 3.10+
sudo apt install python3.10 python3.10-venv python3-pip nginx -y

# Criar usu??rio para aplica????o
sudo adduser horus
sudo usermod -aG sudo horus
su - horus
```

#### 2. Clonar e Configurar

```bash
# Clonar reposit??rio
git clone <repo-url> /home/horus/horus-operacional
cd /home/horus/horus-operacional

# Criar ambiente virtual
python3.10 -m venv venv
source venv/bin/activate

# Instalar depend??ncias
pip install -r requirements.txt
pip install gunicorn
```

#### 3. Configurar Vari??veis de Ambiente

```bash
cp .env.example .env
nano .env
```

Edite o `.env`:
```env
SECRET_KEY=<gere-uma-chave-aleatoria-forte>
FLASK_ENV=production
FLASK_DEBUG=False
DATABASE_URL=postgresql://user:password@localhost/horus_db  # ou SQLite
SESSION_COOKIE_SECURE=True
```

Gerar chave secreta:
```python
python -c "import secrets; print(secrets.token_hex(32))"
```

#### 4. Inicializar Banco

```bash
python init_db.py
```

#### 5. Configurar Gunicorn

Criar `/etc/systemd/system/horus.service`:

```ini
[Unit]
Description=Horus Operacional
After=network.target

[Service]
User=horus
Group=horus
WorkingDirectory=/home/horus/horus-operacional
Environment="PATH=/home/horus/horus-operacional/venv/bin"
ExecStart=/home/horus/horus-operacional/venv/bin/gunicorn --workers 4 --bind 0.0.0.0:8000 run:app

[Install]
WantedBy=multi-user.target
```

Ativar servi??o:
```bash
sudo systemctl daemon-reload
sudo systemctl start horus
sudo systemctl enable horus
sudo systemctl status horus
```

#### 6. Configurar Nginx

Criar `/etc/nginx/sites-available/horus`:

```nginx
server {
    listen 80;
    server_name seu-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /home/horus/horus-operacional/app/static/;
    }

    client_max_body_size 10M;
}
```

Ativar site:
```bash
sudo ln -s /etc/nginx/sites-available/horus /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 7. SSL com Certbot (HTTPS)

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d seu-dominio.com
```

---

### Op????o 2: Docker

#### 1. Criar Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python init_db.py

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "run:app"]
```

#### 2. Criar docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./horus.db:/app/horus.db
      - ./temp_uploads:/app/temp_uploads
    environment:
      - FLASK_ENV=production
      - SECRET_KEY=${SECRET_KEY}
    restart: unless-stopped
```

#### 3. Deploy

```bash
docker-compose up -d
```

---

### Op????o 3: Heroku

#### 1. Criar Procfile

```
web: gunicorn run:app
```

#### 2. Criar runtime.txt

```
python-3.10.12
```

#### 3. Deploy

```bash
heroku login
heroku create horus-operacional
git push heroku main
heroku run python init_db.py
heroku open
```

---

## ???? Checklist de Seguran??a

- [ ] Alterar `SECRET_KEY` para valor aleat??rio forte
- [ ] Alterar senha do admin padr??o
- [ ] Configurar `FLASK_ENV=production`
- [ ] Desativar `FLASK_DEBUG=False`
- [ ] Ativar HTTPS (SSL/TLS)
- [ ] Configurar `SESSION_COOKIE_SECURE=True`
- [ ] Limitar acesso ao banco de dados
- [ ] Configurar firewall (portas 80, 443 apenas)
- [ ] Backups autom??ticos do banco
- [ ] Logs de acesso e erros
- [ ] Rate limiting (nginx/gunicorn)
- [ ] Monitoramento (New Relic, Datadog, etc.)

---

## ???? Banco de Dados

### SQLite (Desenvolvimento/Pequeno Porte)
- **Vantagens**: Zero configura????o, arquivo ??nico, f??cil backup
- **Limita????es**: Concorr??ncia limitada, sem rede

### PostgreSQL (Recomendado para Produ????o)

```bash
# Instalar PostgreSQL
sudo apt install postgresql postgresql-contrib -y

# Criar banco
sudo -u postgres psql
CREATE DATABASE horus_db;
CREATE USER horus_user WITH PASSWORD 'senha-forte';
GRANT ALL PRIVILEGES ON DATABASE horus_db TO horus_user;
\q

# Atualizar .env
DATABASE_URL=postgresql://horus_user:senha-forte@localhost/horus_db
```

---

## ???? Atualiza????es

### Deploy de Nova Vers??o

```bash
cd /home/horus/horus-operacional
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
flask db upgrade  # Se houver migra????es
sudo systemctl restart horus
```

### Backup

```bash
# SQLite
cp horus.db horus_backup_$(date +%Y%m%d).db

# PostgreSQL
pg_dump horus_db > horus_backup_$(date +%Y%m%d).sql
```

---

## ???? Monitoramento

### Logs

```bash
# Ver logs do servi??o
sudo journalctl -u horus -f

# Ver logs do Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### M??tricas

Considere integrar:
- **New Relic** - Monitoramento APM
- **Sentry** - Rastreamento de erros
- **Prometheus + Grafana** - M??tricas customizadas

---

## ???? Troubleshooting

### Erro 502 Bad Gateway
```bash
# Verificar se o Gunicorn est?? rodando
sudo systemctl status horus

# Reiniciar se necess??rio
sudo systemctl restart horus
```

### Banco de dados corrompido
```bash
# Restaurar backup
cp horus_backup_YYYYMMDD.db horus.db

# Ou reinicializar (ATEN????O: perde dados!)
python init_db.py
```

### Problemas de permiss??o
```bash
# Ajustar ownership
sudo chown -R horus:horus /home/horus/horus-operacional
sudo chmod -R 755 /home/horus/horus-operacional
```

---

## ???? Suporte

Para d??vidas sobre deploy, consulte a documenta????o ou entre em contato com o desenvolvedor.

**H??rus Operacional** - Pronto para Produ????o! ????
