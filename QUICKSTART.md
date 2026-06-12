# ✅ Guia de InÜcio RÜpido - Hórus Operacional

Este guia assume que vocÜ jÜ tem Python 3.13+ instalado no Windows.

---

## ✓ Instalação Rápida (5 minutos)

### 1. Abra o PowerShell no diretÜrio do projeto

```powershell
cd C:\Users\Gustavo\Desktop\horus-operacional
```

### 2. Ative o ambiente virtual

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Execute o servidor

```powershell
python run.py
```

### 4. Acesse no navegador

```
http://localhost:5000
```

---

## ✅ Credenciais de Acesso

### Admin (Acesso completo)
- **Email:** `admin@example.com`
- **Senha:** `admin123`

### Supervisor (Pode editar presenÜas)
- **Email:** `nathani@example.com`
- **Senha:** `nathani123`

### Visualizador (Somente leitura)
- **Email:** `visualizador@example.com`
- **Senha:** `visualizador123`

---

## ✅ Primeiro Uso

### 1. FaÜa login como Admin

Use as credenciais acima.

### 2. VÜ para o Quadro Semanal

Clique em "Quadro Semanal" no menu lateral.

### 3. Selecione o projeto

Escolha **"Educaita"** no dropdown.

### 4. Selecione a semana

Escolha **"Semana 25 Ü 15/06 a 19/06"**.

### 5. Clique em "Carregar"

O quadro serÜ preenchido com todos os profissionais começando como "Presente".

### 6. Altere uma presenÜa

Clique em qualquer dropdown e mude para "Falta justificada", "SaÜda antecipada", etc.

### 7. Salve as alterações

Clique em **"Salvar vigÜlia"** no topo.

### 8. Veja os indicadores atualizarem

A assiduidade serÜ recalculada automaticamente!

---

## ✅ Aplicar um Feriado

1. No quadro semanal carregado, clique em **"Aplicar Feriado"**
2. Selecione o dia da semana (ex: Quarta-feira)
3. Digite uma descri✅o (ex: "Corpus Christi")
4. Clique em **"Aplicar"**
5. Todos os profissionais serão marcados como "Feriado" naquele dia
6. Os indicadores serão recalculados

---

## ✅ Exportar para CSV

1. Com o quadro carregado, clique em **"Exportar CSV"**
2. Um arquivo `.csv` serÜ baixado
3. Abra no Excel ou Google Sheets para anÜlise

---

## ✅ Resetar Banco de Dados

Se quiser resetar tudo e começar do zero:

```powershell
# Ative o ambiente virtual
.\venv\Scripts\Activate.ps1

# Apague o banco
Remove-Item instance\horus.db

# Recrie o banco com dados iniciais
python
>>> from app import create_app, db
>>> from app.utils.init_data import init_database
>>> app = create_app()
>>> with app.app_context():
...     db.create_all()
...     init_database()
>>> exit()
```

---

## ✅ Estrutura de Dados Inicial

### Projeto: Educaita
- **Tipo:** Consultoria
- **Cliente:** Cliente X
- **Status:** Ativo

### Profissionais:
1. **AndrÜ Luiz GuimarÜes** (Matrícula: MI34)
2. **Gustavo Zuim** (Matrícula: MI10)
3. **Nathani** (Matrícula: MI11)

### Semana 25:
- **Período:** 15/06/2026 a 19/06/2026
- **Label:** Semana 25
- **Status:** Todos começam "Presente"

---

## ✓ Perguntas Frequentes

### Como adicionar um novo profissional?

1. VÜ para **"Profissionais"** no menu
2. Clique em **"Novo Profissional"**
3. Preencha nome, matrícula e selecione o projeto
4. Salve

### Como criar uma nova semana?

1. No Quadro Semanal, clique em **"Gerar Planejamento"**
2. Selecione o projeto
3. Escolha uma semana futura
4. Informe o rÜtulo (ex: "Semana 26")
5. Clique em **"Gerar"**
6. Todos os profissionais do projeto serão criados como "Presente"

### Como funciona a assiduidade?

```
Assiduidade = (dias_presentes + saÜdas_antecipadas * 0.5) / dias_vêlidos * 100

Dias vêlidos = Total de dias - (Feriados + Folgas + NÜo planejados)
```

**Exemplo:**
- Total: 15 dias (3 profissionais Ü 5 dias)
- 1 falta justificada
- 3 feriados (1 dia Ü 3 profissionais)
- Dias vêlidos: 15 - 3 = 12
- Dias presentes: 11
- Assiduidade: (11 / 12) Ü 100 = **91.67%**

### Quais sÜo os 8 status possÜveis?

1. ✓ **Presente** ✓ Profissional esteve presente o dia todo
2. ✅ **Falta justificada** ✓ Atestado, licenÜa, etc.
3. ✓ **Falta não justificada** ✓ AusÜncia sem justificativa
4. ✅ **SaÜda antecipada** ✓ Saiu mais cedo (conta 0.5 dia)
5. ✅ **Realocado** ✓ Transferido temporariamente para outro projeto
6. ✅ **Feriado** ✓ Dia de feriado nacional/municipal
7. ✅ **Folga** ✓ Dia de descanso programado
8. ✅Ü **NÜo planejado** ✓ Profissional não estava escalado

### Posso deletar uma semana?

NÜo no MVP atual. Para "desfazer" uma semana, vocÜ pode:
- Marcar todos como "NÜo planejado"
- Ou resetar o banco de dados

---

## ✅ Problemas Comuns

### Erro: "Address already in use"

Outro processo estÜ usando a porta 5000. Feche-o ou mude a porta em `run.py`:

```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Erro: "Can't open database file"

O diretÜrio `instance/` não existe. Crie-o:

```powershell
mkdir instance
```

E recrie o banco de dados com os passos da se✅o "Resetar Banco de Dados".

### As mudanças não estão sendo salvas

Verifique:
1. VocÜ estÜ logado como Admin ou Supervisor? (Visualizador não pode editar)
2. VocÜ clicou em "Salvar vigÜlia"?
3. Veja o console do navegador (F12) para erros JavaScript

---

## ✅ PrÜximos Passos

Agora que vocÜ jÜ sabe usar o bÜsico:

1. ✓ Explore os outros menus (Usuários, Projetos, Profissionais)
2. ✓ Veja os **Logs de Auditoria** para ver todas as ações registradas
3. ✓ Acesse **Indicadores** para ver relatÜrios agregados
4. ✓ Teste com diferentes perfis (Admin, Supervisor, Visualizador)
5. ✓ Leia o [`README.md`](README.md) para arquitetura detalhada
6. ✓ Veja o [`TESTE_FUNCIONAL.md`](TESTE_FUNCIONAL.md) para testes validados

---

## ✅ Precisa de Ajuda?

- **Email:** admin@example.com
- **GitHub Issues:** [Criar issue](https://github.com/seu-usuario/horus-operacional/issues)

---

<div align="center">
  <strong>Bom uso! ✅</strong>
</div>
