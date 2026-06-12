# ÜÜÜ? HÜrus Operacional

> **O olho que vÜ a assiduidade**  
> Sistema de controle de presenÜa operacional por projeto

![Status](https://img.shields.io/badge/status-MVP-yellow)
![Python](https://img.shields.io/badge/python-3.10+-blue)
![Flask](https://img.shields.io/badge/flask-3.0-green)
![License](https://img.shields.io/badge/license-MIT-blue)

---

## ÜÜ Sobre o Projeto

O **HÜrus Operacional** Ü um sistema web para controle de assiduidade operacional por projeto. O nome vem da ideia do "olho que acompanha a operaÜÜo" - assim como o olho de HÜrus, sÜmbolo de proteÜÜo e vigilÜncia.

### Conceito Principal: GestÜo por ExceÜÜo

- Ü? Todos os profissionais comeÜam como **Presente** por padrÜo
- Ü? A supervisÜo altera apenas as **exceÜÜes** (faltas, saÜdas, etc.)
- Ü? CÜlculo automÜtico de assiduidade semanal, mensal e acumulada
- Ü? Auditoria completa com logs de alteraÜÜes

---

## ÜÜÜ? Stack TecnolÜgica

### Por que esta stack?

Escolhemos uma stack **simples, robusta e produtiva** para o MVP:

| Tecnologia | VersÜo | Justificativa |
|------------|--------|---------------|
| **Python** | 3.10+ | CÜdigo limpo, lÜgica de negÜcio clara |
| **Flask** | 3.0 | Minimalista mas poderoso, ideal para MVP |
| **SQLite** | 3.x | Zero configuraÜÜo, arquivo Ünico, fÜcil backup |
| **Jinja2** | 3.x | Templates robustos com heranÜa |
| **SQLAlchemy** | 2.x | ORM type-safe, migrations com Alembic |
| **Flask-Login** | 0.6+ | AutenticaÜÜo segura e simples |
| **Bootstrap** | 5.3 | UI responsiva e consistente |

### Alternativas consideradas (e por que nÜo foram escolhidas)

- **Django**: Mais completo, mas pesado demais para este MVP
- **FastAPI**: Excelente, mas foco em APIs REST (nÜo precisamos de SPA)
- **Node.js + Express**: Ütimo, mas preferimos Python para lÜgica de negÜcio
- **PostgreSQL**: Melhor para produÜÜo, mas SQLite Ü perfeito para MVP
- **React/Vue SPA**: Complexidade desnecessÜria - server-side rendering resolve bem

### Quando migrar para outra stack?

Ü? **Manter** se:
- AtÜ 50 usuÜrios simultÜneos
- AtÜ 10.000 registros/mÜs
- AtÜ 5 projetos ativos

ÜÜÜ **Considerar migraÜÜo** quando:
- Mais de 100 usuÜrios simultÜneos Ü? PostgreSQL + caching
- API pÜblica necessÜria Ü? FastAPI ou GraphQL
- Frontend complexo Ü? React + REST API
- Multi-tenant Ü? Arquitetura de microserviÜos

---

## ÜÜ InstalaÜÜo e ConfiguraÜÜo

### PrÜ-requisitos

- Python 3.10 ou superior
- pip (gerenciador de pacotes Python)
- Git

### 1. Clonar o repositÜrio

```bash
git clone <url-do-repositorio>
cd horus-operacional
```

### 2. Criar ambiente virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependÜncias

```bash
pip install -r requirements.txt
```

### 4. Configurar variÜveis de ambiente

```bash
# Copiar arquivo de exemplo
copy .env.example .env    # Windows
cp .env.example .env      # Linux/Mac
```

Edite o arquivo `.env` e altere:
- `SECRET_KEY`: gere uma chave segura
- `ADMIN_EMAIL` e `ADMIN_PASSWORD`: credenciais do admin

### 5. Inicializar banco de dados

```bash
flask init-db
```

Este comando cria:
- Ü? Tabelas do banco
- Ü? UsuÜrio admin
- Ü? UsuÜrios de exemplo (supervisor e visualizador)
- Ü? Projetos de exemplo
- Ü? Profissionais de exemplo

### 6. Rodar a aplicaÜÜo

```bash
python run.py
```

Ou usando Flask CLI:

```bash
flask run
```

Acesse: **http://localhost:5000**

---

## ÜÜ UsuÜrios de Teste

ApÜs inicializar o banco, vocÜ terÜ:

| Perfil | Email | Senha | PermissÜes |
|--------|-------|-------|------------|
| **Admin** | admin@horus.local | admin123 | Acesso total |
| **Supervisor** | nathani@horus.local | supervisor123 | Editar quadros, indicadores |
| **Visualizador** | viewer@horus.local | viewer123 | Apenas visualizar |

ÜÜÜ **Importante**: Troque estas senhas antes de colocar em produÜÜo!

---

## ÜÜ Arquitetura do Sistema

### Estrutura de Pastas

```
horus-operacional/
ÜÜÜÜ? app/
Ü?   ÜÜÜÜ? __init__.py          # Factory da aplicaÜÜo
Ü?   ÜÜÜÜ? models.py            # Modelos SQLAlchemy
Ü?   ÜÜÜÜ? routes/
Ü?   Ü?   ÜÜÜÜ? __init__.py
Ü?   Ü?   ÜÜÜÜ? auth.py          # Rotas de autenticaÜÜo
Ü?   Ü?   ÜÜÜÜ? main.py          # Rotas principais
Ü?   ÜÜÜÜ? templates/           # Templates Jinja2
Ü?   Ü?   ÜÜÜÜ? base.html        # Template base
Ü?   Ü?   ÜÜÜÜ? index.html       # Landing page
Ü?   Ü?   ÜÜÜÜ? dashboard.html   # Dashboard principal
Ü?   Ü?   ÜÜÜÜ? auth/
Ü?   Ü?       ÜÜÜÜ? login.html   # PÜgina de login
Ü?   ÜÜÜÜ? static/
Ü?   Ü?   ÜÜÜÜ? css/
Ü?   Ü?   Ü?   ÜÜÜÜ? horus.css    # Estilos customizados
Ü?   Ü?   ÜÜÜÜ? js/
Ü?   Ü?       ÜÜÜÜ? horus.js     # JavaScript core
Ü?   ÜÜÜÜ? utils/
Ü?       ÜÜÜÜ? init_data.py     # Dados iniciais
ÜÜÜÜ? config.py                # ConfiguraÜÜes
ÜÜÜÜ? run.py                   # Entrada da aplicaÜÜo
ÜÜÜÜ? requirements.txt         # DependÜncias
ÜÜÜÜ? .env.example             # Exemplo de variÜveis
ÜÜÜÜ? .gitignore
ÜÜÜÜ? README.md
```

### Modelo de Dados

```
users
ÜÜÜ id
ÜÜÜ email (unique)
ÜÜÜ password_hash
ÜÜÜ name
ÜÜÜ role (admin/supervisor/visualizador)
ÜÜÜ active

projects                     planning_weeks
ÜÜÜ id                       ÜÜÜ id
ÜÜÜ name                     ÜÜÜ project_id (FK)
ÜÜÜ code (unique)            ÜÜÜ week_number
ÜÜÜ active                   ÜÜÜ week_start (segunda)
                            ÜÜÜ week_end (sexta)
                            ÜÜÜ created_by (FK users)
                                    Ü?
professionals                       ÜÜÜÜ? planning_allocations
ÜÜÜ id                              ÜÜÜ id
ÜÜÜ name                            ÜÜÜ planning_week_id (FK)
ÜÜÜ registration (unique)           ÜÜÜ professional_id (FK)
ÜÜÜ role_description                ÜÜÜ observation
ÜÜÜ active                                  Ü?
                                          ÜÜÜÜ? daily_statuses
                                              ÜÜÜ id
                                              ÜÜÜ allocation_id (FK)
                                              ÜÜÜ date
                                              ÜÜÜ status (enum)
                                              ÜÜÜ observation
                                              ÜÜÜ updated_by (FK users)
                                              ÜÜÜ updated_at
```

### Regras de NegÜcio

#### Status DisponÜveis

1. Ü? **Presente** (padrÜo)
2. ÜÜ **Falta justificada**
3. Ü? **Falta nÜo justificada**
4. Ü? **SaÜda antecipada**
5. ÜÜ **Realocado**
6. ÜÜ **Feriado**
7. ÜÜÜ? **Folga**
8. ÜÜ **NÜo planejado**

#### CÜlculo de Assiduidade

**Entram no denominador** (dias vÜlidos):
- Presente
- Falta justificada
- Falta nÜo justificada
- SaÜda antecipada
- Realocado

**NÜo entram no denominador**:
- Feriado
- Folga
- NÜo planejado

**Contam como presenÜa**:
- Ü? Presente
- Ü? SaÜda antecipada
- Ü? Realocado

**FÜrmula**:
```
taxa_assiduidade = (dias_presentes / dias_validos) Ü 100

Se dias_validos = 0, exibir "N/A"
```

### Perfis de UsuÜrio

#### ÜÜ Admin
- Acessa tudo
- Cadastra usuÜrios, projetos e profissionais
- Gera planejamentos
- Edita quadro semanal
- Aplica feriados
- VÜ indicadores e logs

#### ÜÜÜ? Supervisor
- Acessa dashboard
- Acessa quadro semanal
- Altera status dos profissionais
- Pode gerar/importar planejamento (se permitido)
- Aplica feriados
- VÜ indicadores

#### ÜÜ Visualizador
- Acessa dashboard
- VÜ indicadores
- **NÜo edita nada**

---

## ÜÜ SeguranÜa

Ü? Senhas com hash bcrypt (Werkzeug)  
Ü? Flask-Login para sessÜes seguras  
Ü? ProteÜÜo CSRF em formulÜrios  
Ü? Cookies HttpOnly e SameSite  
Ü? SQLAlchemy protege contra SQL injection  
Ü? Logs de auditoria (quem alterou o quÜ)  

ÜÜÜ **Antes de produÜÜo**:
- [ ] Trocar `SECRET_KEY` por valor forte
- [ ] Configurar `SESSION_COOKIE_SECURE=True` (requer HTTPS)
- [ ] Migrar para PostgreSQL
- [ ] Configurar rate limiting
- [ ] Habilitar HTTPS
- [ ] Revisar permissÜes de usuÜrios

---

## ÜÜ ImportaÜÜo de Planejamento em PDF

### VisÜo Geral

O sistema permite **upload semanal de planejamentos em PDF** com prÜvia revisÜvel antes da gravaÜÜo. Isso evita digitaÜÜo manual e garante seguranÜa na importaÜÜo.

### Fluxo de ImportaÜÜo

```
1. Upload do PDF Ü? 2. ExtraÜÜo de texto Ü? 3. Parser inteligente Ü? 
4. PrÜvia editÜvel Ü? 5. ConfirmaÜÜo Ü? 6. GeraÜÜo do quadro semanal
```

### Biblioteca Utilizada

**PyMuPDF (fitz)** - Escolhida por:
- Ü? RÜpida e eficiente
- Ü? Extrai texto diretamente (sem OCR)
- Ü? Bem mantida e documentada
- Ü? LicenÜa compatÜvel (AGPL)

### Como Usar

#### 1. Acessar ImportaÜÜo
- Menu lateral Ü? **Importar planejamento**
- Apenas **Admin** e **Supervisor** tÜm acesso

#### 2. Fazer Upload
1. Selecionar projeto
2. Fazer upload do arquivo PDF (mÜx. 10MB)
3. Clicar em "Processar PDF"

#### 3. Revisar PrÜvia
O sistema tenta identificar automaticamente:
- Ü? NÜmero da semana (ex: "Semana 25")
- Ü? Datas (dd/mm/yyyy)
- Ü? Profissionais cadastrados
- Ü? MatrÜculas
- Ü? Feriados e folgas

**Alertas exibidos:**
- ÜÜÜ Semana nÜo identificada Ü? preencher manualmente
- ÜÜÜ Datas nÜo identificadas Ü? preencher manualmente
- ÜÜÜ Profissionais nÜo encontrados no PDF
- ÜÜÜ Profissionais ativos nÜo identificados

#### 4. Editar Status
Na tabela de prÜvia, vocÜ pode:
- Alterar status de qualquer dia (Segunda a Sexta)
- Adicionar observaÜÜes
- Corrigir dados automaticamente identificados

#### 5. Confirmar ImportaÜÜo
- Clicar em "Confirmar importaÜÜo"
- Sistema gera quadro semanal no banco
- Redirecionamento automÜtico para visualizar

### Parser Inteligente

O parser busca no texto do PDF:

| Elemento | PadrÜo de Busca | Exemplo |
|----------|-----------------|---------|
| Semana | `Semana (\d+)` | "Semana 25" |
| Datas | `dd/mm/yyyy` | 15/06/2026 |
| MatrÜcula | `[A-Z]{2}\d+` | MI34, PM001 |
| Feriado | palavra "feriado" | "Quarta: Feriado" |
| Folga | palavra "folga" | "Quinta: Folga" |

### Regras de ImportaÜÜo

Ü? **PadrÜo Ü "Presente"**: Todos os dias comeÜam como Presente  
Ü? **Feriado para todos**: Se identificar feriado em um dia, aplica a todos os profissionais  
Ü? **Folga individual**: Revisar manualmente na prÜvia  
Ü? **Profissionais novos**: Alertar se encontrar matrÜcula nÜo cadastrada  
Ü? **NÜo sobrescrever**: Se jÜ existe planejamento da mesma semana, avisa e bloqueia  

### LimitaÜÜes Conhecidas

Ü? **NÜo faz OCR**: Apenas extrai texto jÜ digitÜvel do PDF  
Ü? **PDFs escaneados**: NÜo funcionam (texto Ü imagem)  
Ü? **Layouts muito complexos**: Parser pode nÜo identificar tudo  
Ü? **Tabelas complexas**: Melhor revisar a prÜvia  

**SoluÜÜo**: A prÜvia editÜvel permite corrigir qualquer problema antes da gravaÜÜo.

### Criar PDF de Teste

Use o script fornecido:

```bash
# Instalar biblioteca
pip install reportlab

# Gerar PDF de exemplo
python create_sample_pdf.py
```

Isso cria `exemplo_planejamento_semana25.pdf` com:
- Semana 25
- PerÜodo: 15/06/2026 a 19/06/2026
- 3 profissionais (AndrÜ, Gustavo, Nathani)
- Feriado na quarta-feira (Corpus Christi)
- Folga para Nathani na quinta

### Melhorias Futuras

- [ ] Suporte a OCR para PDFs escaneados (Tesseract)
- [ ] Parser mais inteligente com ML
- [ ] Mapeamento de layouts customizados por projeto
- [ ] ImportaÜÜo de atividades planejadas (alÜm de status)
- [ ] Preview com diff se jÜ existir planejamento
- [ ] HistÜrico de arquivos importados

---

## ÜÜ Testando a AplicaÜÜo

### Health Check

```bash
curl http://localhost:5000/health
```

Resposta esperada:
```json
{
  "status": "ok",
  "app": "HÜrus Operacional",
  "version": "1.0.0"
}
```

### Testando AutenticaÜÜo

1. Acesse: http://localhost:5000
2. Clique em "Entrar na vigÜlia"
3. Use um dos usuÜrios de teste
4. Verifique o dashboard

### Testando PermissÜes

- **Como Visualizador**: nÜo deve ver "Importar" nem "Salvar"
- **Como Supervisor**: deve ver quadro editÜvel
- **Como Admin**: deve ver menu de "Cadastros"

---

## ÜÜ Deploy

### OpÜÜes Recomendadas

| Plataforma | PrÜs | Contras | Custo |
|------------|------|---------|-------|
| **Railway** | Setup fÜcil, PostgreSQL grÜtis | Limite de horas grÜtis | $5/mÜs |
| **Render** | CI/CD automÜtico, SSL grÜtis | Cold start em plano free | $7/mÜs |
| **PythonAnywhere** | Simples, Python nativo | Menos flexÜvel | $5/mÜs |
| **Fly.io** | Global, PostgreSQL incluÜdo | ConfiguraÜÜo manual | $0-10/mÜs |
| **Heroku** | Maduro, muitos addons | Caro | $7/mÜs |

### Deploy no Railway (Recomendado)

```bash
# 1. Instalar Railway CLI
npm install -g @railway/cli

# 2. Login
railway login

# 3. Criar projeto
railway init

# 4. Adicionar PostgreSQL
railway add postgresql

# 5. Deploy
railway up
```

### Deploy no Render

1. Conectar repositÜrio GitHub
2. Configurar:
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn run:app`
3. Adicionar PostgreSQL database
4. Configurar variÜveis de ambiente
5. Deploy automÜtico!

---

## ÜÜÜ? PrÜximos Passos de ImplementaÜÜo

Este MVP contÜm a base funcional. As prÜximas etapas sÜo:

### Fase 1 - Core Funcional (Semana 1-2)
- [ ] Criar planejamento semanal (CRUD)
- [ ] Gerar quadro semanal com profissionais
- [ ] Editar status dos dias (grid interativo)
- [ ] Aplicar feriado em lote
- [ ] CÜlculo de assiduidade em tempo real

### Fase 2 - GestÜo (Semana 3)
- [ ] CRUD de Projetos
- [ ] CRUD de Profissionais
- [ ] CRUD de UsuÜrios (admin)
- [ ] ValidaÜÜes de formulÜrios

### Fase 3 - Indicadores (Semana 4)
- [ ] RelatÜrio semanal
- [ ] RelatÜrio mensal
- [ ] RelatÜrio por perÜodo customizado
- [ ] Exportar CSV
- [ ] GrÜficos de tendÜncia

### Fase 4 - Auditoria e Melhorias (Semana 5)
- [ ] Logs de alteraÜÜes
- [ ] ObservaÜÜes por dia/profissional
- [ ] Filtros avanÜados
- [ ] Busca de profissionais
- [ ] PaginaÜÜo

### Fase 5 - ProduÜÜo (Semana 6)
- [ ] MigraÜÜo para PostgreSQL
- [ ] Testes automatizados
- [ ] CI/CD
- [ ] Backup automÜtico
- [ ] Monitoramento
- [ ] DocumentaÜÜo de API

---

## ÜÜ Comandos Üteis

```bash
# Ativar ambiente virtual
venv\Scripts\activate          # Windows
source venv/bin/activate       # Linux/Mac

# Instalar dependÜncias
pip install -r requirements.txt

# Inicializar banco
flask init-db

# Rodar aplicaÜÜo
python run.py
flask run                      # alternativa

# Flask shell (interativo)
flask shell

# Criar migraÜÜo (apÜs alterar models)
flask db init                  # primeira vez
flask db migrate -m "descriÜÜo"
flask db upgrade

# Rodar em modo debug
export FLASK_ENV=development   # Linux/Mac
set FLASK_ENV=development      # Windows
flask run --debug

# Rodar em porta diferente
flask run --port 8000
```

---

## ÜÜ Contribuindo

Este Ü um MVP em desenvolvimento. SugestÜes e melhorias sÜo bem-vindas!

### Reportar Bugs

Abra uma issue com:
- DescriÜÜo do problema
- Passos para reproduzir
- Comportamento esperado vs. atual
- Screenshots (se aplicÜvel)

### Sugerir Features

Use issues com label `enhancement`:
- Descreva o caso de uso
- BenefÜcios esperados
- Mockups (opcional)

---

## ÜÜ LicenÜa

MIT License - veja [LICENSE](LICENSE) para detalhes.

---

## ÜÜ Autores

Desenvolvido como MVP para controle de assiduidade operacional.

**VersÜo**: 1.0.0 (MVP)  
**Status**: Em desenvolvimento ativo  
**Ültima atualizaÜÜo**: Junho 2026

---

## ÜÜ Agradecimentos

- Bootstrap pela UI responsiva
- Flask pela simplicidade e poder
- SQLAlchemy pela excelente abstraÜÜo de banco
- A equipe operacional que inspirou este sistema

---

**ÜÜÜ? Que o olho de HÜrus vigie suas operaÜÜes!**
