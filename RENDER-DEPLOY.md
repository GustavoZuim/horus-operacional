# ÜÜ Deploy no Render.com (GRATUITO)

Guia rÜpido para fazer deploy do **HÜrus Operacional** no Render.com gratuitamente.

## ÜÜ PrÜ-requisitos

1. Conta no GitHub (para conectar o repositÜrio)
2. Conta no Render.com (criar em: https://render.com)

---

## ÜÜ Passo a Passo

### 1ÜÜÜ Preparar o RepositÜrio GitHub

Se ainda nÜo tem repositÜrio Git:

```bash
cd C:\Users\Gustavo\Desktop\horus-operacional

# Inicializar git (se ainda nÜo foi)
git init

# Adicionar todos os arquivos
git add .

# Fazer commit
git commit -m "Deploy: Projeto HÜrus Operacional pronto"

# Criar repositÜrio no GitHub e conectar
# (VÜ em github.com e crie um novo repositÜrio)
git remote add origin https://github.com/SEU-USUARIO/horus-operacional.git
git branch -M main
git push -u origin main
```

### 2ÜÜÜ Criar Conta no Render

1. Acesse: https://render.com
2. Clique em **"Get Started"** ou **"Sign Up"**
3. Conecte com sua conta do **GitHub**
4. Autorize o Render a acessar seus repositÜrios

### 3ÜÜÜ Criar Web Service

1. No dashboard do Render, clique em **"New +"**
2. Selecione **"Web Service"**
3. Conecte seu repositÜrio **horus-operacional**
4. Configure:
   - **Name**: `horus-operacional`
   - **Region**: `Frankfurt (EU Central)` ou mais prÜximo de vocÜ
   - **Branch**: `main`
   - **Root Directory**: (deixe vazio)
   - **Runtime**: `Python 3`
   - **Build Command**: `bash build.sh`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT run:app`
   - **Instance Type**: **Free** (750 horas/mÜs grÜtis)

5. Em **Environment Variables**, adicione:
   ```
   FLASK_ENV=production
   SECRET_KEY=(deixe o Render gerar automaticamente)
   ```

6. Clique em **"Create Web Service"**

### 4ÜÜÜ Aguardar Deploy

O Render vai:
1. Ü? Clonar seu repositÜrio
2. Ü? Instalar dependÜncias (`pip install -r requirements.txt`)
3. Ü? Executar `build.sh` (que roda `init_db.py`)
4. Ü? Iniciar a aplicaÜÜo com Gunicorn

**Tempo estimado: 2-5 minutos**

### 5ÜÜÜ Acessar a AplicaÜÜo

Quando o deploy terminar, vocÜ verÜ:
- Ü? Status: **Live**
- ÜÜ URL: `https://horus-operacional-xxxx.onrender.com`

**Clique na URL para acessar!**

---

## ÜÜ Primeiro Acesso

Credenciais padrÜo:
- **Email**: `admin@horus.local`
- **Senha**: `admin123`

ÜÜÜ **IMPORTANTE**: Altere a senha imediatamente apÜs o primeiro login!

---

## ÜÜ Plano Gratuito

### Limites do Plano Free:
- Ü? **750 horas/mÜs** (suficiente se nÜo rodar 24/7)
- Ü? **512 MB RAM**
- Ü? **100 GB largura de banda/mÜs**
- Ü? **SSL/HTTPS automÜtico**
- Ü? **DomÜnio .onrender.com grÜtis**
- ÜÜÜ **O serviÜo "dorme" apÜs 15 min de inatividade** (primeiro acesso demora ~30s)

### Como Manter Ativo 24/7 (Opcional)

Se quiser que nunca durma, use um serviÜo de "ping" grÜtis:
- **UptimeRobot** (https://uptimerobot.com) - Faz ping a cada 5 minutos
- **Cron-job.org** (https://cron-job.org) - Faz ping periÜdico

---

## ÜÜ AtualizaÜÜes

Para fazer deploy de uma nova versÜo:

```bash
# Fazer alteraÜÜes no cÜdigo
git add .
git commit -m "DescriÜÜo das mudanÜas"
git push

# O Render detecta automaticamente e faz redeploy!
```

---

## ÜÜ DomÜnio Personalizado (Opcional)

Se tiver um domÜnio prÜprio:
1. VÜ em **Settings** > **Custom Domain**
2. Adicione seu domÜnio (ex: `horus.seudominio.com`)
3. Configure o DNS conforme instruÜÜes do Render
4. SSL serÜ configurado automaticamente!

---

## ÜÜ Monitoramento

No dashboard do Render vocÜ pode ver:
- ÜÜ Logs em tempo real
- ÜÜ Uso de memÜria
- ÜÜ TrÜfego de rede
- Ü? Status do serviÜo

---

## ÜÜ Problemas Comuns

### Deploy falhou
- Verifique os **logs** no dashboard do Render
- Confira se `requirements.txt` estÜ correto
- Certifique-se que `build.sh` tem permissÜo de execuÜÜo

### AplicaÜÜo nÜo inicia
- Verifique se `run.py` existe e estÜ correto
- Confira as variÜveis de ambiente
- Veja os logs de startup

### Banco de dados vazio
- O `build.sh` roda `init_db.py` automaticamente
- Se precisar reinicializar, adicione manualmente no dashboard

---

## ÜÜ Dicas

1. **Use o plano gratuito** para testes e MVPs
2. **Monitore** o uso no dashboard
3. **Habilite notificaÜÜes** de deploy no Render
4. **Configure variÜveis de ambiente** sensÜveis no Render (nÜo no cÜdigo)
5. **FaÜa backup** regular do banco de dados

---

## ÜÜ Upgrade (Opcional)

Se precisar de mais recursos:
- **Starter**: $7/mÜs - Nunca dorme, mais RAM
- **Standard**: $25/mÜs - Ainda mais recursos
- **Pro**: $85/mÜs - MÜximo desempenho

---

## Ü? Checklist Final

- [ ] RepositÜrio no GitHub criado e com push
- [ ] Conta no Render criada e conectada ao GitHub
- [ ] Web Service criado com configuraÜÜes corretas
- [ ] Deploy concluÜdo com sucesso (status: Live)
- [ ] AplicaÜÜo acessÜvel via URL do Render
- [ ] Login funcionando com credenciais padrÜo
- [ ] Senha do admin alterada

---

## ÜÜ Pronto!

Sua aplicaÜÜo **HÜrus Operacional** estÜ no ar e acessÜvel publicamente!

**URL**: DisponÜvel no dashboard do Render

**Qualquer dÜvida**: Consulte a documentaÜÜo do Render em https://render.com/docs

---

**HÜrus Operacional** - Deploy FÜcil e Gratuito! ÜÜ
