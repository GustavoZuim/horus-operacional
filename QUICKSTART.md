# ???? Guia de In??cio R??pido - H??rus Operacional

Este guia assume que voc?? j?? tem Python 3.13+ instalado no Windows.

---

## ??? Instala????o R??pida (5 minutos)

### 1. Abra o PowerShell no diret??rio do projeto

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

## ???? Credenciais de Acesso

### Admin (Acesso completo)
- **Email:** `admin@example.com`
- **Senha:** `admin123`

### Supervisor (Pode editar presen??as)
- **Email:** `nathani@example.com`
- **Senha:** `nathani123`

### Visualizador (Somente leitura)
- **Email:** `visualizador@example.com`
- **Senha:** `visualizador123`

---

## ???? Primeiro Uso

### 1. Fa??a login como Admin

Use as credenciais acima.

### 2. V?? para o Quadro Semanal

Clique em "Quadro Semanal" no menu lateral.

### 3. Selecione o projeto

Escolha **"Educaita"** no dropdown.

### 4. Selecione a semana

Escolha **"Semana 25 ?? 15/06 a 19/06"**.

### 5. Clique em "Carregar"

O quadro ser?? preenchido com todos os profissionais come??ando como "Presente".

### 6. Altere uma presen??a

Clique em qualquer dropdown e mude para "Falta justificada", "Sa??da antecipada", etc.

### 7. Salve as altera????es

Clique em **"Salvar vig??lia"** no topo.

### 8. Veja os indicadores atualizarem

A assiduidade ser?? recalculada automaticamente!

---

## ???? Aplicar um Feriado

1. No quadro semanal carregado, clique em **"Aplicar Feriado"**
2. Selecione o dia da semana (ex: Quarta-feira)
3. Digite uma descri????o (ex: "Corpus Christi")
4. Clique em **"Aplicar"**
5. Todos os profissionais ser??o marcados como "Feriado" naquele dia
6. Os indicadores ser??o recalculados

---

## ???? Exportar para CSV

1. Com o quadro carregado, clique em **"Exportar CSV"**
2. Um arquivo `.csv` ser?? baixado
3. Abra no Excel ou Google Sheets para an??lise

---

## ???? Resetar Banco de Dados

Se quiser resetar tudo e come??ar do zero:

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

## ???? Estrutura de Dados Inicial

### Projeto: Educaita
- **Tipo:** Consultoria
- **Cliente:** Cliente X
- **Status:** Ativo

### Profissionais:
1. **Andr?? Luiz Guimar??es** (Matr??cula: MI34)
2. **Gustavo Zuim** (Matr??cula: MI10)
3. **Nathani** (Matr??cula: MI11)

### Semana 25:
- **Per??odo:** 15/06/2026 a 19/06/2026
- **Label:** Semana 25
- **Status:** Todos come??am "Presente"

---

## ??? Perguntas Frequentes

### Como adicionar um novo profissional?

1. V?? para **"Profissionais"** no menu
2. Clique em **"Novo Profissional"**
3. Preencha nome, matr??cula e selecione o projeto
4. Salve

### Como criar uma nova semana?

1. No Quadro Semanal, clique em **"Gerar Planejamento"**
2. Selecione o projeto
3. Escolha uma semana futura
4. Informe o r??tulo (ex: "Semana 26")
5. Clique em **"Gerar"**
6. Todos os profissionais do projeto ser??o criados como "Presente"

### Como funciona a assiduidade?

```
Assiduidade = (dias_presentes + sa??das_antecipadas * 0.5) / dias_v??lidos * 100

Dias v??lidos = Total de dias - (Feriados + Folgas + N??o planejados)
```

**Exemplo:**
- Total: 15 dias (3 profissionais ?? 5 dias)
- 1 falta justificada
- 3 feriados (1 dia ?? 3 profissionais)
- Dias v??lidos: 15 - 3 = 12
- Dias presentes: 11
- Assiduidade: (11 / 12) ?? 100 = **91.67%**

### Quais s??o os 8 status poss??veis?

1. ??? **Presente** ??? Profissional esteve presente o dia todo
2. ???? **Falta justificada** ??? Atestado, licen??a, etc.
3. ??? **Falta n??o justificada** ??? Aus??ncia sem justificativa
4. ???? **Sa??da antecipada** ??? Saiu mais cedo (conta 0.5 dia)
5. ???? **Realocado** ??? Transferido temporariamente para outro projeto
6. ???? **Feriado** ??? Dia de feriado nacional/municipal
7. ???? **Folga** ??? Dia de descanso programado
8. ?????? **N??o planejado** ??? Profissional n??o estava escalado

### Posso deletar uma semana?

N??o no MVP atual. Para "desfazer" uma semana, voc?? pode:
- Marcar todos como "N??o planejado"
- Ou resetar o banco de dados

---

## ???? Problemas Comuns

### Erro: "Address already in use"

Outro processo est?? usando a porta 5000. Feche-o ou mude a porta em `run.py`:

```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Erro: "Can't open database file"

O diret??rio `instance/` n??o existe. Crie-o:

```powershell
mkdir instance
```

E recrie o banco de dados com os passos da se????o "Resetar Banco de Dados".

### As mudan??as n??o est??o sendo salvas

Verifique:
1. Voc?? est?? logado como Admin ou Supervisor? (Visualizador n??o pode editar)
2. Voc?? clicou em "Salvar vig??lia"?
3. Veja o console do navegador (F12) para erros JavaScript

---

## ???? Pr??ximos Passos

Agora que voc?? j?? sabe usar o b??sico:

1. ??? Explore os outros menus (Usu??rios, Projetos, Profissionais)
2. ??? Veja os **Logs de Auditoria** para ver todas as a????es registradas
3. ??? Acesse **Indicadores** para ver relat??rios agregados
4. ??? Teste com diferentes perfis (Admin, Supervisor, Visualizador)
5. ??? Leia o [`README.md`](README.md) para arquitetura detalhada
6. ??? Veja o [`TESTE_FUNCIONAL.md`](TESTE_FUNCIONAL.md) para testes validados

---

## ???? Precisa de Ajuda?

- **Email:** admin@example.com
- **GitHub Issues:** [Criar issue](https://github.com/seu-usuario/horus-operacional/issues)

---

<div align="center">
  <strong>Bom uso! ????</strong>
</div>
