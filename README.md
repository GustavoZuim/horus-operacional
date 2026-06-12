# ??????? H??rus Operacional

> **O olho que v?? a assiduidade**  
> Sistema de controle de presen??a operacional por projeto

![Status](https://img.shields.io/badge/status-MVP-yellow)
![Python](https://img.shields.io/badge/python-3.10+-blue)
![Flask](https://img.shields.io/badge/flask-3.0-green)
![License](https://img.shields.io/badge/license-MIT-blue)

---

## ???? Sobre o Projeto

O **H??rus Operacional** ?? um sistema web para controle de assiduidade operacional por projeto. O nome vem da ideia do "olho que acompanha a opera????o" - assim como o olho de H??rus, s??mbolo de prote????o e vigil??ncia.

### Conceito Principal: Gest??o por Exce????o

- ??? Todos os profissionais come??am como **Presente** por padr??o
- ??? A supervis??o altera apenas as **exce????es** (faltas, sa??das, etc.)
- ??? C??lculo autom??tico de assiduidade semanal, mensal e acumulada
- ??? Auditoria completa com logs de altera????es

---

## ??????? Stack Tecnol??gica

### Por que esta stack?

Escolhemos uma stack **simples, robusta e produtiva** para o MVP:

| Tecnologia | Vers??o | Justificativa |
|------------|--------|---------------|
| **Python** | 3.10+ | C??digo limpo, l??gica de neg??cio clara |
| **Flask** | 3.0 | Minimalista mas poderoso, ideal para MVP |
| **SQLite** | 3.x | Zero configura????o, arquivo ??nico, f??cil backup |
| **Jinja2** | 3.x | Templates robustos com heran??a |
| **SQLAlchemy** | 2.x | ORM type-safe, migrations com Alembic |
| **Flask-Login** | 0.6+ | Autentica????o segura e simples |
| **Bootstrap** | 5.3 | UI responsiva e consistente |

### Alternativas consideradas (e por que n??o foram escolhidas)

- **Django**: Mais completo, mas pesado demais para este MVP
- **FastAPI**: Excelente, mas foco em APIs REST (n??o precisamos de SPA)
- **Node.js + Express**: ??timo, mas preferimos Python para l??gica de neg??cio
- **PostgreSQL**: Melhor para produ????o, mas SQLite ?? perfeito para MVP
- **React/Vue SPA**: Complexidade desnecess??ria - server-side rendering resolve bem

### Quando migrar para outra stack?

??? **Manter** se:
- At?? 50 usu??rios simult??neos
- At?? 10.000 registros/m??s
- At?? 5 projetos ativos

?????? **Considerar migra????o** quando:
- Mais de 100 usu??rios simult??neos ??? PostgreSQL + caching
- API p??blica necess??ria ??? FastAPI ou GraphQL
- Frontend complexo ??? React + REST API
- Multi-tenant ??? Arquitetura de microservi??os

---

## ???? Instala????o e Configura????o

### Pr??-requisitos

- Python 3.10 ou superior
- pip (gerenciador de pacotes Python)
- Git

### 1. Clonar o reposit??rio

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

### 3. Instalar depend??ncias

```bash
pip install -r requirements.txt
```

### 4. Configurar vari??veis de ambiente

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
- ??? Tabelas do banco
- ??? Usu??rio admin
- ??? Usu??rios de exemplo (supervisor e visualizador)
- ??? Projetos de exemplo
- ??? Profissionais de exemplo

### 6. Rodar a aplica????o

```bash
python run.py
```

Ou usando Flask CLI:

```bash
flask run
```

Acesse: **http://localhost:5000**

---

## ???? Usu??rios de Teste

Ap??s inicializar o banco, voc?? ter??:

| Perfil | Email | Senha | Permiss??es |
|--------|-------|-------|------------|
| **Admin** | admin@horus.local | admin123 | Acesso total |
| **Supervisor** | nathani@horus.local | supervisor123 | Editar quadros, indicadores |
| **Visualizador** | viewer@horus.local | viewer123 | Apenas visualizar |

?????? **Importante**: Troque estas senhas antes de colocar em produ????o!

---

## ???? Arquitetura do Sistema

### Estrutura de Pastas

```
horus-operacional/
????????? app/
???   ????????? __init__.py          # Factory da aplica????o
???   ????????? models.py            # Modelos SQLAlchemy
???   ????????? routes/
???   ???   ????????? __init__.py
???   ???   ????????? auth.py          # Rotas de autentica????o
???   ???   ????????? main.py          # Rotas principais
???   ????????? templates/           # Templates Jinja2
???   ???   ????????? base.html        # Template base
???   ???   ????????? index.html       # Landing page
???   ???   ????????? dashboard.html   # Dashboard principal
???   ???   ????????? auth/
???   ???       ????????? login.html   # P??gina de login
???   ????????? static/
???   ???   ????????? css/
???   ???   ???   ????????? horus.css    # Estilos customizados
???   ???   ????????? js/
???   ???       ????????? horus.js     # JavaScript core
???   ????????? utils/
???       ????????? init_data.py     # Dados iniciais
????????? config.py                # Configura????es
????????? run.py                   # Entrada da aplica????o
????????? requirements.txt         # Depend??ncias
????????? .env.example             # Exemplo de vari??veis
????????? .gitignore
????????? README.md
```

### Modelo de Dados

```
users
?????? id
?????? email (unique)
?????? password_hash
?????? name
?????? role (admin/supervisor/visualizador)
?????? active

projects                     planning_weeks
?????? id                       ?????? id
?????? name                     ?????? project_id (FK)
?????? code (unique)            ?????? week_number
?????? active                   ?????? week_start (segunda)
                            ?????? week_end (sexta)
                            ?????? created_by (FK users)
                                    ???
professionals                       ????????? planning_allocations
?????? id                              ?????? id
?????? name                            ?????? planning_week_id (FK)
?????? registration (unique)           ?????? professional_id (FK)
?????? role_description                ?????? observation
?????? active                                  ???
                                          ????????? daily_statuses
                                              ?????? id
                                              ?????? allocation_id (FK)
                                              ?????? date
                                              ?????? status (enum)
                                              ?????? observation
                                              ?????? updated_by (FK users)
                                              ?????? updated_at
```

### Regras de Neg??cio

#### Status Dispon??veis

1. ??? **Presente** (padr??o)
2. ???? **Falta justificada**
3. ??? **Falta n??o justificada**
4. ??? **Sa??da antecipada**
5. ???? **Realocado**
6. ???? **Feriado**
7. ??????? **Folga**
8. ???? **N??o planejado**

#### C??lculo de Assiduidade

**Entram no denominador** (dias v??lidos):
- Presente
- Falta justificada
- Falta n??o justificada
- Sa??da antecipada
- Realocado

**N??o entram no denominador**:
- Feriado
- Folga
- N??o planejado

**Contam como presen??a**:
- ??? Presente
- ??? Sa??da antecipada
- ??? Realocado

**F??rmula**:
```
taxa_assiduidade = (dias_presentes / dias_validos) ?? 100

Se dias_validos = 0, exibir "N/A"
```

### Perfis de Usu??rio

#### ???? Admin
- Acessa tudo
- Cadastra usu??rios, projetos e profissionais
- Gera planejamentos
- Edita quadro semanal
- Aplica feriados
- V?? indicadores e logs

#### ??????? Supervisor
- Acessa dashboard
- Acessa quadro semanal
- Altera status dos profissionais
- Pode gerar/importar planejamento (se permitido)
- Aplica feriados
- V?? indicadores

#### ???? Visualizador
- Acessa dashboard
- V?? indicadores
- **N??o edita nada**

---

## ???? Seguran??a

??? Senhas com hash bcrypt (Werkzeug)  
??? Flask-Login para sess??es seguras  
??? Prote????o CSRF em formul??rios  
??? Cookies HttpOnly e SameSite  
??? SQLAlchemy protege contra SQL injection  
??? Logs de auditoria (quem alterou o qu??)  

?????? **Antes de produ????o**:
- [ ] Trocar `SECRET_KEY` por valor forte
- [ ] Configurar `SESSION_COOKIE_SECURE=True` (requer HTTPS)
- [ ] Migrar para PostgreSQL
- [ ] Configurar rate limiting
- [ ] Habilitar HTTPS
- [ ] Revisar permiss??es de usu??rios

---

## ???? Importa????o de Planejamento em PDF

### Vis??o Geral

O sistema permite **upload semanal de planejamentos em PDF** com pr??via revis??vel antes da grava????o. Isso evita digita????o manual e garante seguran??a na importa????o.

### Fluxo de Importa????o

```
1. Upload do PDF ??? 2. Extra????o de texto ??? 3. Parser inteligente ??? 
4. Pr??via edit??vel ??? 5. Confirma????o ??? 6. Gera????o do quadro semanal
```

### Biblioteca Utilizada

**PyMuPDF (fitz)** - Escolhida por:
- ??? R??pida e eficiente
- ??? Extrai texto diretamente (sem OCR)
- ??? Bem mantida e documentada
- ??? Licen??a compat??vel (AGPL)

### Como Usar

#### 1. Acessar Importa????o
- Menu lateral ??? **Importar planejamento**
- Apenas **Admin** e **Supervisor** t??m acesso

#### 2. Fazer Upload
1. Selecionar projeto
2. Fazer upload do arquivo PDF (m??x. 10MB)
3. Clicar em "Processar PDF"

#### 3. Revisar Pr??via
O sistema tenta identificar automaticamente:
- ??? N??mero da semana (ex: "Semana 25")
- ??? Datas (dd/mm/yyyy)
- ??? Profissionais cadastrados
- ??? Matr??culas
- ??? Feriados e folgas

**Alertas exibidos:**
- ?????? Semana n??o identificada ??? preencher manualmente
- ?????? Datas n??o identificadas ??? preencher manualmente
- ?????? Profissionais n??o encontrados no PDF
- ?????? Profissionais ativos n??o identificados

#### 4. Editar Status
Na tabela de pr??via, voc?? pode:
- Alterar status de qualquer dia (Segunda a Sexta)
- Adicionar observa????es
- Corrigir dados automaticamente identificados

#### 5. Confirmar Importa????o
- Clicar em "Confirmar importa????o"
- Sistema gera quadro semanal no banco
- Redirecionamento autom??tico para visualizar

### Parser Inteligente

O parser busca no texto do PDF:

| Elemento | Padr??o de Busca | Exemplo |
|----------|-----------------|---------|
| Semana | `Semana (\d+)` | "Semana 25" |
| Datas | `dd/mm/yyyy` | 15/06/2026 |
| Matr??cula | `[A-Z]{2}\d+` | MI34, PM001 |
| Feriado | palavra "feriado" | "Quarta: Feriado" |
| Folga | palavra "folga" | "Quinta: Folga" |

### Regras de Importa????o

??? **Padr??o ?? "Presente"**: Todos os dias come??am como Presente  
??? **Feriado para todos**: Se identificar feriado em um dia, aplica a todos os profissionais  
??? **Folga individual**: Revisar manualmente na pr??via  
??? **Profissionais novos**: Alertar se encontrar matr??cula n??o cadastrada  
??? **N??o sobrescrever**: Se j?? existe planejamento da mesma semana, avisa e bloqueia  

### Limita????es Conhecidas

??? **N??o faz OCR**: Apenas extrai texto j?? digit??vel do PDF  
??? **PDFs escaneados**: N??o funcionam (texto ?? imagem)  
??? **Layouts muito complexos**: Parser pode n??o identificar tudo  
??? **Tabelas complexas**: Melhor revisar a pr??via  

**Solu????o**: A pr??via edit??vel permite corrigir qualquer problema antes da grava????o.

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
- Per??odo: 15/06/2026 a 19/06/2026
- 3 profissionais (Andr??, Gustavo, Nathani)
- Feriado na quarta-feira (Corpus Christi)
- Folga para Nathani na quinta

### Melhorias Futuras

- [ ] Suporte a OCR para PDFs escaneados (Tesseract)
- [ ] Parser mais inteligente com ML
- [ ] Mapeamento de layouts customizados por projeto
- [ ] Importa????o de atividades planejadas (al??m de status)
- [ ] Preview com diff se j?? existir planejamento
- [ ] Hist??rico de arquivos importados

---

## ???? Testando a Aplica????o

### Health Check

```bash
curl http://localhost:5000/health
```

Resposta esperada:
```json
{
  "status": "ok",
  "app": "H??rus Operacional",
  "version": "1.0.0"
}
```

### Testando Autentica????o

1. Acesse: http://localhost:5000
2. Clique em "Entrar na vig??lia"
3. Use um dos usu??rios de teste
4. Verifique o dashboard

### Testando Permiss??es

- **Como Visualizador**: n??o deve ver "Importar" nem "Salvar"
- **Como Supervisor**: deve ver quadro edit??vel
- **Como Admin**: deve ver menu de "Cadastros"

---

## ???? Deploy

### Op????es Recomendadas

| Plataforma | Pr??s | Contras | Custo |
|------------|------|---------|-------|
| **Railway** | Setup f??cil, PostgreSQL gr??tis | Limite de horas gr??tis | $5/m??s |
| **Render** | CI/CD autom??tico, SSL gr??tis | Cold start em plano free | $7/m??s |
| **PythonAnywhere** | Simples, Python nativo | Menos flex??vel | $5/m??s |
| **Fly.io** | Global, PostgreSQL inclu??do | Configura????o manual | $0-10/m??s |
| **Heroku** | Maduro, muitos addons | Caro | $7/m??s |

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

1. Conectar reposit??rio GitHub
2. Configurar:
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn run:app`
3. Adicionar PostgreSQL database
4. Configurar vari??veis de ambiente
5. Deploy autom??tico!

---

## ??????? Pr??ximos Passos de Implementa????o

Este MVP cont??m a base funcional. As pr??ximas etapas s??o:

### Fase 1 - Core Funcional (Semana 1-2)
- [ ] Criar planejamento semanal (CRUD)
- [ ] Gerar quadro semanal com profissionais
- [ ] Editar status dos dias (grid interativo)
- [ ] Aplicar feriado em lote
- [ ] C??lculo de assiduidade em tempo real

### Fase 2 - Gest??o (Semana 3)
- [ ] CRUD de Projetos
- [ ] CRUD de Profissionais
- [ ] CRUD de Usu??rios (admin)
- [ ] Valida????es de formul??rios

### Fase 3 - Indicadores (Semana 4)
- [ ] Relat??rio semanal
- [ ] Relat??rio mensal
- [ ] Relat??rio por per??odo customizado
- [ ] Exportar CSV
- [ ] Gr??ficos de tend??ncia

### Fase 4 - Auditoria e Melhorias (Semana 5)
- [ ] Logs de altera????es
- [ ] Observa????es por dia/profissional
- [ ] Filtros avan??ados
- [ ] Busca de profissionais
- [ ] Pagina????o

### Fase 5 - Produ????o (Semana 6)
- [ ] Migra????o para PostgreSQL
- [ ] Testes automatizados
- [ ] CI/CD
- [ ] Backup autom??tico
- [ ] Monitoramento
- [ ] Documenta????o de API

---

## ???? Comandos ??teis

```bash
# Ativar ambiente virtual
venv\Scripts\activate          # Windows
source venv/bin/activate       # Linux/Mac

# Instalar depend??ncias
pip install -r requirements.txt

# Inicializar banco
flask init-db

# Rodar aplica????o
python run.py
flask run                      # alternativa

# Flask shell (interativo)
flask shell

# Criar migra????o (ap??s alterar models)
flask db init                  # primeira vez
flask db migrate -m "descri????o"
flask db upgrade

# Rodar em modo debug
export FLASK_ENV=development   # Linux/Mac
set FLASK_ENV=development      # Windows
flask run --debug

# Rodar em porta diferente
flask run --port 8000
```

---

## ???? Contribuindo

Este ?? um MVP em desenvolvimento. Sugest??es e melhorias s??o bem-vindas!

### Reportar Bugs

Abra uma issue com:
- Descri????o do problema
- Passos para reproduzir
- Comportamento esperado vs. atual
- Screenshots (se aplic??vel)

### Sugerir Features

Use issues com label `enhancement`:
- Descreva o caso de uso
- Benef??cios esperados
- Mockups (opcional)

---

## ???? Licen??a

MIT License - veja [LICENSE](LICENSE) para detalhes.

---

## ???? Autores

Desenvolvido como MVP para controle de assiduidade operacional.

**Vers??o**: 1.0.0 (MVP)  
**Status**: Em desenvolvimento ativo  
**??ltima atualiza????o**: Junho 2026

---

## ???? Agradecimentos

- Bootstrap pela UI responsiva
- Flask pela simplicidade e poder
- SQLAlchemy pela excelente abstra????o de banco
- A equipe operacional que inspirou este sistema

---

**??????? Que o olho de H??rus vigie suas opera????es!**
