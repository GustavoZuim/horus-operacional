# 🗑️ Hórus Operacional

> **O olho que vê a assiduidade**  
> Sistema de controle de presenÜa operacional por projeto

![Status](https://img.shields.io/badge/status-MVP-yellow)
![Python](https://img.shields.io/badge/python-3.10+-blue)
![Flask](https://img.shields.io/badge/flask-3.0-green)
![License](https://img.shields.io/badge/license-MIT-blue)

---

## ✅ Sobre o Projeto

O **Hórus Operacional** Ü um sistema web para controle de assiduidade operacional por projeto. O nome vem da ideia do "olho que acompanha a operação" - assim como o olho de Hórus, símbolo de proteção e vigilÜncia.

### Conceito Principal: Gestão por Exceção

- ✓ Todos os profissionais começam como **Presente** por padrÜo
- ✓ A supervisÜo altera apenas as **exce✅es** (faltas, saÜdas, etc.)
- ✓ CÜlculo automÜtico de assiduidade semanal, mensal e acumulada
- ✓ Auditoria completa com logs de alterações

---

## 🗑️ Stack TecnolÜgica

### Por que esta stack?

Escolhemos uma stack **simples, robusta e produtiva** para o MVP:

| Tecnologia | VersÜo | Justificativa |
|------------|--------|---------------|
| **Python** | 3.10+ | CÜdigo limpo, lÜgica de negÜcio clara |
| **Flask** | 3.0 | Minimalista mas poderoso, ideal para MVP |
| **SQLite** | 3.x | Zero configuração, arquivo Ünico, fÜcil backup |
| **Jinja2** | 3.x | Templates robustos com heranÜa |
| **SQLAlchemy** | 2.x | ORM type-safe, migrations com Alembic |
| **Flask-Login** | 0.6+ | Autenticação segura e simples |
| **Bootstrap** | 5.3 | UI responsiva e consistente |

### Alternativas consideradas (e por que não foram escolhidas)

- **Django**: Mais completo, mas pesado demais para este MVP
- **FastAPI**: Excelente, mas foco em APIs REST (não precisamos de SPA)
- **Node.js + Express**: Ütimo, mas preferimos Python para lÜgica de negÜcio
- **PostgreSQL**: Melhor para produção, mas SQLite Ü perfeito para MVP
- **React/Vue SPA**: Complexidade desnecessÜria - server-side rendering resolve bem

### Quando migrar para outra stack?

✓ **Manter** se:
- AtÜ 50 usuários simultÜneos
- AtÜ 10.000 registros/mÜs
- AtÜ 5 projetos ativos

✅Ü **Considerar migração** quando:
- Mais de 100 usuários simultÜneos ✓ PostgreSQL + caching
- API pÜblica necessÜria ✓ FastAPI ou GraphQL
- Frontend complexo ✓ React + REST API
- Multi-tenant ✓ Arquitetura de microserviÜos

---

## ✅ Instalação e Configuração

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
- ✓ Tabelas do banco
- ✓ Usuário admin
- ✓ Usuários de exemplo (supervisor e visualizador)
- ✓ Projetos de exemplo
- ✓ Profissionais de exemplo

### 6. Rodar a aplicação

```bash
python run.py
```

Ou usando Flask CLI:

```bash
flask run
```

Acesse: **http://localhost:5000**

---

## ✅ Usuários de Teste

ApÜs inicializar o banco, vocÜ terÜ:

| Perfil | Email | Senha | PermissÜes |
|--------|-------|-------|------------|
| **Admin** | admin@horus.local | admin123 | Acesso total |
| **Supervisor** | nathani@horus.local | supervisor123 | Editar quadros, indicadores |
| **Visualizador** | viewer@horus.local | viewer123 | Apenas visualizar |

✅Ü **Importante**: Troque estas senhas antes de colocar em produção!

---

## ✅ Arquitetura do Sistema

### Estrutura de Pastas

```
horus-operacional/
Ü🗑️ app/
✓   Ü🗑️ __init__.py          # Factory da aplicação
✓   Ü🗑️ models.py            # Modelos SQLAlchemy
✓   Ü🗑️ routes/
✓   ✓   Ü🗑️ __init__.py
✓   ✓   Ü🗑️ auth.py          # Rotas de autenticação
✓   ✓   Ü🗑️ main.py          # Rotas principais
✓   Ü🗑️ templates/           # Templates Jinja2
✓   ✓   Ü🗑️ base.html        # Template base
✓   ✓   Ü🗑️ index.html       # Landing page
✓   ✓   Ü🗑️ dashboard.html   # Dashboard principal
✓   ✓   Ü🗑️ auth/
✓   ✓       Ü🗑️ login.html   # PÜgina de login
✓   Ü🗑️ static/
✓   ✓   Ü🗑️ css/
✓   ✓   ✓   Ü🗑️ horus.css    # Estilos customizados
✓   ✓   Ü🗑️ js/
✓   ✓       Ü🗑️ horus.js     # JavaScript core
✓   Ü🗑️ utils/
✓       Ü🗑️ init_data.py     # Dados iniciais
Ü🗑️ config.py                # Configurações
Ü🗑️ run.py                   # Entrada da aplicação
Ü🗑️ requirements.txt         # DependÜncias
Ü🗑️ .env.example             # Exemplo de variÜveis
Ü🗑️ .gitignore
Ü🗑️ README.md
```

### Modelo de Dados

```
users
✅Ü id
✅Ü email (unique)
✅Ü password_hash
✅Ü name
✅Ü role (admin/supervisor/visualizador)
✅Ü active

projects                     planning_weeks
✅Ü id                       ✅Ü id
✅Ü name                     ✅Ü project_id (FK)
✅Ü code (unique)            ✅Ü week_number
✅Ü active                   ✅Ü week_start (segunda)
                            ✅Ü week_end (sexta)
                            ✅Ü created_by (FK users)
                                    ✓
professionals                       Ü🗑️ planning_allocations
✅Ü id                              ✅Ü id
✅Ü name                            ✅Ü planning_week_id (FK)
✅Ü registration (unique)           ✅Ü professional_id (FK)
✅Ü role_description                ✅Ü observation
✅Ü active                                  ✓
                                          Ü🗑️ daily_statuses
                                              ✅Ü id
                                              ✅Ü allocation_id (FK)
                                              ✅Ü date
                                              ✅Ü status (enum)
                                              ✅Ü observation
                                              ✅Ü updated_by (FK users)
                                              ✅Ü updated_at
```

### Regras de NegÜcio

#### Status DisponÜveis

1. ✓ **Presente** (padrÜo)
2. ✅ **Falta justificada**
3. ✓ **Falta não justificada**
4. ✓ **SaÜda antecipada**
5. ✅ **Realocado**
6. ✅ **Feriado**
7. 🗑️ **Folga**
8. ✅ **NÜo planejado**

#### CÜlculo de Assiduidade

**Entram no denominador** (dias vêlidos):
- Presente
- Falta justificada
- Falta não justificada
- SaÜda antecipada
- Realocado

**NÜo entram no denominador**:
- Feriado
- Folga
- NÜo planejado

**Contam como presenÜa**:
- ✓ Presente
- ✓ SaÜda antecipada
- ✓ Realocado

**FÜrmula**:
```
taxa_assiduidade = (dias_presentes / dias_validos) Ü 100

Se dias_validos = 0, exibir "N/A"
```

### Perfis de Usuário

#### ✅ Admin
- Acessa tudo
- Cadastra usuários, projetos e profissionais
- Gera planejamentos
- Edita quadro semanal
- Aplica feriados
- VÜ indicadores e logs

#### 🗑️ Supervisor
- Acessa dashboard
- Acessa quadro semanal
- Altera status dos profissionais
- Pode gerar/importar planejamento (se permitido)
- Aplica feriados
- VÜ indicadores

#### ✅ Visualizador
- Acessa dashboard
- VÜ indicadores
- **NÜo edita nada**

---

## ✅ SeguranÜa

✓ Senhas com hash bcrypt (Werkzeug)  
✓ Flask-Login para sessÜes seguras  
✓ Prote✅o CSRF em formulários  
✓ Cookies HttpOnly e SameSite  
✓ SQLAlchemy protege contra SQL injection  
✓ Logs de auditoria (quem alterou o quÜ)  

✅Ü **Antes de produção**:
- [ ] Trocar `SECRET_KEY` por valor forte
- [ ] Configurar `SESSION_COOKIE_SECURE=True` (requer HTTPS)
- [ ] Migrar para PostgreSQL
- [ ] Configurar rate limiting
- [ ] Habilitar HTTPS
- [ ] Revisar permissÜes de usuários

---

## ✅ Importação de Planejamento em PDF

### VisÜo Geral

O sistema permite **upload semanal de planejamentos em PDF** com prévia revisível antes da gravação. Isso evita digitação manual e garante seguranÜa na importação.

### Fluxo de Importação

```
1. Upload do PDF ✓ 2. Extração de texto ✓ 3. Parser inteligente ✓ 
4. Prévia editÜvel ✓ 5. Confirmação ✓ 6. Geração do quadro semanal
```

### Biblioteca Utilizada

**PyMuPDF (fitz)** - Escolhida por:
- ✓ Rápida e eficiente
- ✓ Extrai texto diretamente (sem OCR)
- ✓ Bem mantida e documentada
- ✓ LicenÜa compatÜvel (AGPL)

### Como Usar

#### 1. Acessar Importação
- Menu lateral ✓ **Importar planejamento**
- Apenas **Admin** e **Supervisor** tÜm acesso

#### 2. Fazer Upload
1. Selecionar projeto
2. Fazer upload do arquivo PDF (mÜx. 10MB)
3. Clicar em "Processar PDF"

#### 3. Revisar Prévia
O sistema tenta identificar automaticamente:
- ✓ NÜmero da semana (ex: "Semana 25")
- ✓ Datas (dd/mm/yyyy)
- ✓ Profissionais cadastrados
- ✓ Matrículas
- ✓ Feriados e folgas

**Alertas exibidos:**
- ✅Ü Semana não identificada ✓ preencher manualmente
- ✅Ü Datas não identificadas ✓ preencher manualmente
- ✅Ü Profissionais não encontrados no PDF
- ✅Ü Profissionais ativos não identificados

#### 4. Editar Status
Na tabela de prévia, vocÜ pode:
- Alterar status de qualquer dia (Segunda a Sexta)
- Adicionar observações
- Corrigir dados automaticamente identificados

#### 5. Confirmar Importação
- Clicar em "Confirmar importação"
- Sistema gera quadro semanal no banco
- Redirecionamento automÜtico para visualizar

### Parser Inteligente

O parser busca no texto do PDF:

| Elemento | PadrÜo de Busca | Exemplo |
|----------|-----------------|---------|
| Semana | `Semana (\d+)` | "Semana 25" |
| Datas | `dd/mm/yyyy` | 15/06/2026 |
| Matrícula | `[A-Z]{2}\d+` | MI34, PM001 |
| Feriado | palavra "feriado" | "Quarta: Feriado" |
| Folga | palavra "folga" | "Quinta: Folga" |

### Regras de Importação

✓ **PadrÜo Ü "Presente"**: Todos os dias começam como Presente  
✓ **Feriado para todos**: Se identificar feriado em um dia, aplica a todos os profissionais  
✓ **Folga individual**: Revisar manualmente na prévia  
✓ **Profissionais novos**: Alertar se encontrar matrícula não cadastrada  
✓ **NÜo sobrescrever**: Se jÜ existe planejamento da mesma semana, avisa e bloqueia  

### Limitações Conhecidas

✓ **NÜo faz OCR**: Apenas extrai texto jÜ digitÜvel do PDF  
✓ **PDFs escaneados**: NÜo funcionam (texto Ü imagem)  
✓ **Layouts muito complexos**: Parser pode não identificar tudo  
✓ **Tabelas complexas**: Melhor revisar a prévia  

**Solu✅o**: A prévia editÜvel permite corrigir qualquer problema antes da gravação.

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
- Período: 15/06/2026 a 19/06/2026
- 3 profissionais (AndrÜ, Gustavo, Nathani)
- Feriado na quarta-feira (Corpus Christi)
- Folga para Nathani na quinta

### Melhorias Futuras

- [ ] Suporte a OCR para PDFs escaneados (Tesseract)
- [ ] Parser mais inteligente com ML
- [ ] Mapeamento de layouts customizados por projeto
- [ ] Importação de atividades planejadas (alÜm de status)
- [ ] Preview com diff se jÜ existir planejamento
- [ ] HistÜrico de arquivos importados

---

## ✅ Testando a Aplicação

### Health Check

```bash
curl http://localhost:5000/health
```

Resposta esperada:
```json
{
  "status": "ok",
  "app": "Hórus Operacional",
  "version": "1.0.0"
}
```

### Testando Autenticação

1. Acesse: http://localhost:5000
2. Clique em "Entrar na vigÜlia"
3. Use um dos usuários de teste
4. Verifique o dashboard

### Testando PermissÜes

- **Como Visualizador**: não deve ver "Importar" nem "Salvar"
- **Como Supervisor**: deve ver quadro editÜvel
- **Como Admin**: deve ver menu de "Cadastros"

---

## ✅ Deploy

### Op✅es Recomendadas

| Plataforma | PrÜs | Contras | Custo |
|------------|------|---------|-------|
| **Railway** | Setup fÜcil, PostgreSQL grÜtis | Limite de horas grÜtis | $5/mÜs |
| **Render** | CI/CD automÜtico, SSL grÜtis | Cold start em plano free | $7/mÜs |
| **PythonAnywhere** | Simples, Python nativo | Menos flexÜvel | $5/mÜs |
| **Fly.io** | Global, PostgreSQL incluÜdo | Configuração manual | $0-10/mÜs |
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

## 🗑️ PrÜximos Passos de Implementação

Este MVP contÜm a base funcional. As prÜximas etapas sÜo:

### Fase 1 - Core Funcional (Semana 1-2)
- [ ] Criar planejamento semanal (CRUD)
- [ ] Gerar quadro semanal com profissionais
- [ ] Editar status dos dias (grid interativo)
- [ ] Aplicar feriado em lote
- [ ] CÜlculo de assiduidade em tempo real

### Fase 2 - Gestão (Semana 3)
- [ ] CRUD de Projetos
- [ ] CRUD de Profissionais
- [ ] CRUD de Usuários (admin)
- [ ] Validações de formulários

### Fase 3 - Indicadores (Semana 4)
- [ ] RelatÜrio semanal
- [ ] RelatÜrio mensal
- [ ] RelatÜrio por período customizado
- [ ] Exportar CSV
- [ ] GrÜficos de tendÜncia

### Fase 4 - Auditoria e Melhorias (Semana 5)
- [ ] Logs de alterações
- [ ] Observações por dia/profissional
- [ ] Filtros avanÜados
- [ ] Busca de profissionais
- [ ] Paginação

### Fase 5 - Produção (Semana 6)
- [ ] Migração para PostgreSQL
- [ ] Testes automatizados
- [ ] CI/CD
- [ ] Backup automÜtico
- [ ] Monitoramento
- [ ] Documentação de API

---

## ✅ Comandos Üteis

```bash
# Ativar ambiente virtual
venv\Scripts\activate          # Windows
source venv/bin/activate       # Linux/Mac

# Instalar dependÜncias
pip install -r requirements.txt

# Inicializar banco
flask init-db

# Rodar aplicação
python run.py
flask run                      # alternativa

# Flask shell (interativo)
flask shell

# Criar migração (apÜs alterar models)
flask db init                  # primeira vez
flask db migrate -m "descri✅o"
flask db upgrade

# Rodar em modo debug
export FLASK_ENV=development   # Linux/Mac
set FLASK_ENV=development      # Windows
flask run --debug

# Rodar em porta diferente
flask run --port 8000
```

---

## ✅ Contribuindo

Este Ü um MVP em desenvolvimento. SugestÜes e melhorias sÜo bem-vindas!

### Reportar Bugs

Abra uma issue com:
- Descri✅o do problema
- Passos para reproduzir
- Comportamento esperado vs. atual
- Screenshots (se aplicÜvel)

### Sugerir Features

Use issues com label `enhancement`:
- Descreva o caso de uso
- BenefÜcios esperados
- Mockups (opcional)

---

## ✅ LicenÜa

MIT License - veja [LICENSE](LICENSE) para detalhes.

---

## ✅ Autores

Desenvolvido como MVP para controle de assiduidade operacional.

**VersÜo**: 1.0.0 (MVP)  
**Status**: Em desenvolvimento ativo  
**Ültima atualização**: Junho 2026

---

## ✅ Agradecimentos

- Bootstrap pela UI responsiva
- Flask pela simplicidade e poder
- SQLAlchemy pela excelente abstração de banco
- A equipe operacional que inspirou este sistema

---

**🗑️ Que o olho de Hórus vigie suas operações!**
