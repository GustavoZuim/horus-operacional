# ÜÜ Guia de Deploy - HÜrus Operacional

## Ü? Quick Start (Desenvolvimento)

```bash
# 1. Clone e entre no diretÜrio
cd horus-operacional

# 2. Crie o ambiente virtual
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 3. Instale dependÜncias
pip install -r requirements.txt

# 4. Inicialize o banco de dados
python init_db.py

# 5. Execute
python run.py
```

**Credenciais padrÜo:**
- Email: `admin@horus.local`
- Senha: `admin123`

ÜÜÜ **Altere a senha apÜs o primeiro login!**

---

## ÜÜ Deploy em ProduÜÜo

### OpÜÜo 1: VPS/Servidor Linux

#### 1. Preparar o Servidor

```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Python 3.10+
sudo apt install python3.10 python3.10-venv python3-pip nginx -y

# Criar usuÜrio para aplicaÜÜo
sudo adduser horus
sudo usermod -aG sudo horus
su - horus
```

#### 2. Clonar e Configurar

```bash
# Clonar repositÜrio
git clone <repo-url> /home/horus/horus-operacional
cd /home/horus/horus-operacional

# Criar ambiente virtual
python3.10 -m venv venv
source venv/bin/activate

# Instalar dependÜncias
pip install -r requirements.txt
pip install gunicorn
```

#### 3. Configurar VariÜveis de Ambiente

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

Ativar serviÜo:
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

### OpÜÜo 2: Docker

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

### OpÜÜo 3: Heroku

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

## ÜÜ Checklist de SeguranÜa

- [ ] Alterar `SECRET_KEY` para valor aleatÜrio forte
- [ ] Alterar senha do admin padrÜo
- [ ] Configurar `FLASK_ENV=production`
- [ ] Desativar `FLASK_DEBUG=False`
- [ ] Ativar HTTPS (SSL/TLS)
- [ ] Configurar `SESSION_COOKIE_SECURE=True`
- [ ] Limitar acesso ao banco de dados
- [ ] Configurar firewall (portas 80, 443 apenas)
- [ ] Backups automÜticos do banco
- [ ] Logs de acesso e erros
- [ ] Rate limiting (nginx/gunicorn)
- [ ] Monitoramento (New Relic, Datadog, etc.)

---

## ÜÜ Banco de Dados

### SQLite (Desenvolvimento/Pequeno Porte)
- **Vantagens**: Zero configuraÜÜo, arquivo Ünico, fÜcil backup
- **LimitaÜÜes**: ConcorrÜncia limitada, sem rede

### PostgreSQL (Recomendado para ProduÜÜo)

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

## ÜÜ AtualizaÜÜes

### Deploy de Nova VersÜo

```bash
cd /home/horus/horus-operacional
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
flask db upgrade  # Se houver migraÜÜes
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

## ÜÜ Monitoramento

### Logs

```bash
# Ver logs do serviÜo
sudo journalctl -u horus -f

# Ver logs do Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### MÜtricas

Considere integrar:
- **New Relic** - Monitoramento APM
- **Sentry** - Rastreamento de erros
- **Prometheus + Grafana** - MÜtricas customizadas

---

## ÜÜ Troubleshooting

### Erro 502 Bad Gateway
```bash
# Verificar se o Gunicorn estÜ rodando
sudo systemctl status horus

# Reiniciar se necessÜrio
sudo systemctl restart horus
```

### Banco de dados corrompido
```bash
# Restaurar backup
cp horus_backup_YYYYMMDD.db horus.db

# Ou reinicializar (ATENÜÜO: perde dados!)
python init_db.py
```

### Problemas de permissÜo
```bash
# Ajustar ownership
sudo chown -R horus:horus /home/horus/horus-operacional
sudo chmod -R 755 /home/horus/horus-operacional
```

---

## ÜÜ Suporte

Para dÜvidas sobre deploy, consulte a documentaÜÜo ou entre em contato com o desenvolvedor.

**HÜrus Operacional** - Pronto para ProduÜÜo! ÜÜ
