# ???? Deploy no Render.com (GRATUITO)

Guia r??pido para fazer deploy do **H??rus Operacional** no Render.com gratuitamente.

## ???? Pr??-requisitos

1. Conta no GitHub (para conectar o reposit??rio)
2. Conta no Render.com (criar em: https://render.com)

---

## ???? Passo a Passo

### 1?????? Preparar o Reposit??rio GitHub

Se ainda n??o tem reposit??rio Git:

```bash
cd C:\Users\Gustavo\Desktop\horus-operacional

# Inicializar git (se ainda n??o foi)
git init

# Adicionar todos os arquivos
git add .

# Fazer commit
git commit -m "Deploy: Projeto H??rus Operacional pronto"

# Criar reposit??rio no GitHub e conectar
# (V?? em github.com e crie um novo reposit??rio)
git remote add origin https://github.com/SEU-USUARIO/horus-operacional.git
git branch -M main
git push -u origin main
```

### 2?????? Criar Conta no Render

1. Acesse: https://render.com
2. Clique em **"Get Started"** ou **"Sign Up"**
3. Conecte com sua conta do **GitHub**
4. Autorize o Render a acessar seus reposit??rios

### 3?????? Criar Web Service

1. No dashboard do Render, clique em **"New +"**
2. Selecione **"Web Service"**
3. Conecte seu reposit??rio **horus-operacional**
4. Configure:
   - **Name**: `horus-operacional`
   - **Region**: `Frankfurt (EU Central)` ou mais pr??ximo de voc??
   - **Branch**: `main`
   - **Root Directory**: (deixe vazio)
   - **Runtime**: `Python 3`
   - **Build Command**: `bash build.sh`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT run:app`
   - **Instance Type**: **Free** (750 horas/m??s gr??tis)

5. Em **Environment Variables**, adicione:
   ```
   FLASK_ENV=production
   SECRET_KEY=(deixe o Render gerar automaticamente)
   ```

6. Clique em **"Create Web Service"**

### 4?????? Aguardar Deploy

O Render vai:
1. ??? Clonar seu reposit??rio
2. ??? Instalar depend??ncias (`pip install -r requirements.txt`)
3. ??? Executar `build.sh` (que roda `init_db.py`)
4. ??? Iniciar a aplica????o com Gunicorn

**Tempo estimado: 2-5 minutos**

### 5?????? Acessar a Aplica????o

Quando o deploy terminar, voc?? ver??:
- ??? Status: **Live**
- ???? URL: `https://horus-operacional-xxxx.onrender.com`

**Clique na URL para acessar!**

---

## ???? Primeiro Acesso

Credenciais padr??o:
- **Email**: `admin@horus.local`
- **Senha**: `admin123`

?????? **IMPORTANTE**: Altere a senha imediatamente ap??s o primeiro login!

---

## ???? Plano Gratuito

### Limites do Plano Free:
- ??? **750 horas/m??s** (suficiente se n??o rodar 24/7)
- ??? **512 MB RAM**
- ??? **100 GB largura de banda/m??s**
- ??? **SSL/HTTPS autom??tico**
- ??? **Dom??nio .onrender.com gr??tis**
- ?????? **O servi??o "dorme" ap??s 15 min de inatividade** (primeiro acesso demora ~30s)

### Como Manter Ativo 24/7 (Opcional)

Se quiser que nunca durma, use um servi??o de "ping" gr??tis:
- **UptimeRobot** (https://uptimerobot.com) - Faz ping a cada 5 minutos
- **Cron-job.org** (https://cron-job.org) - Faz ping peri??dico

---

## ???? Atualiza????es

Para fazer deploy de uma nova vers??o:

```bash
# Fazer altera????es no c??digo
git add .
git commit -m "Descri????o das mudan??as"
git push

# O Render detecta automaticamente e faz redeploy!
```

---

## ???? Dom??nio Personalizado (Opcional)

Se tiver um dom??nio pr??prio:
1. V?? em **Settings** > **Custom Domain**
2. Adicione seu dom??nio (ex: `horus.seudominio.com`)
3. Configure o DNS conforme instru????es do Render
4. SSL ser?? configurado automaticamente!

---

## ???? Monitoramento

No dashboard do Render voc?? pode ver:
- ???? Logs em tempo real
- ???? Uso de mem??ria
- ???? Tr??fego de rede
- ??? Status do servi??o

---

## ???? Problemas Comuns

### Deploy falhou
- Verifique os **logs** no dashboard do Render
- Confira se `requirements.txt` est?? correto
- Certifique-se que `build.sh` tem permiss??o de execu????o

### Aplica????o n??o inicia
- Verifique se `run.py` existe e est?? correto
- Confira as vari??veis de ambiente
- Veja os logs de startup

### Banco de dados vazio
- O `build.sh` roda `init_db.py` automaticamente
- Se precisar reinicializar, adicione manualmente no dashboard

---

## ???? Dicas

1. **Use o plano gratuito** para testes e MVPs
2. **Monitore** o uso no dashboard
3. **Habilite notifica????es** de deploy no Render
4. **Configure vari??veis de ambiente** sens??veis no Render (n??o no c??digo)
5. **Fa??a backup** regular do banco de dados

---

## ???? Upgrade (Opcional)

Se precisar de mais recursos:
- **Starter**: $7/m??s - Nunca dorme, mais RAM
- **Standard**: $25/m??s - Ainda mais recursos
- **Pro**: $85/m??s - M??ximo desempenho

---

## ??? Checklist Final

- [ ] Reposit??rio no GitHub criado e com push
- [ ] Conta no Render criada e conectada ao GitHub
- [ ] Web Service criado com configura????es corretas
- [ ] Deploy conclu??do com sucesso (status: Live)
- [ ] Aplica????o acess??vel via URL do Render
- [ ] Login funcionando com credenciais padr??o
- [ ] Senha do admin alterada

---

## ???? Pronto!

Sua aplica????o **H??rus Operacional** est?? no ar e acess??vel publicamente!

**URL**: Dispon??vel no dashboard do Render

**Qualquer d??vida**: Consulte a documenta????o do Render em https://render.com/docs

---

**H??rus Operacional** - Deploy F??cil e Gratuito! ????
