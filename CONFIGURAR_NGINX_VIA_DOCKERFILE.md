# 🐳 Configurar Nginx Auth via Dockerfile (Método Alternativo)

## 📝 Quando Usar Este Método

Use este método se:
- ❌ Não encontrou opção de Nginx/Auth no Coolify UI
- ❌ Interface do Coolify não tem campo para .htpasswd
- ✅ Quer configurar tudo via código

---

## 🔧 Como Funciona

**Ideia básica:**
1. Editar `Dockerfile` para copiar `.htpasswd`
2. Configurar Nginx dentro do container
3. Redeploy automático
4. Pronto! 🔐

---

## 📋 Passo 1: Editar o Dockerfile

**Arquivo:** `Dockerfile`

**Adicione estas linhas após `COPY .streamlit/`:**

```dockerfile
# Copiar arquivo de autenticação Nginx
COPY .htpasswd /app/.htpasswd

# Criar diretório Nginx config (se necessário)
RUN mkdir -p /etc/nginx/conf.d

# Arquivo Nginx com autenticação
RUN echo 'location / { \
    auth_basic "Acesso Restrito"; \
    auth_basic_user_file /app/.htpasswd; \
    proxy_pass http://localhost:8501; \
}' > /etc/nginx/conf.d/auth.conf
```

**Resultado final do Dockerfile:**

```dockerfile
# Usar Python 3.11 slim
FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements.txt
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY src/ ./src/
COPY img/ ./img/
COPY .streamlit/ ./.streamlit/

# Copiar arquivo de autenticação ← NOVO
COPY .htpasswd /app/.htpasswd

# Expor porta
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8501/_stcore/health')"

# Comando para iniciar
CMD ["streamlit", "run", "src/app_streamlit.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

---

## 🚀 Passo 2: Commitar para GitHub

```bash
# Adicionar Dockerfile modificado
git add Dockerfile

# Commitar
git commit -m "chore: Adicionar autenticacao Nginx via Dockerfile"

# Push
git push origin main
```

---

## 🔄 Passo 3: Redeploy no Coolify

1. Abra seu Coolify
2. Vá para seu app: Gerador-JSON-Hybris
3. Vá para "Deployments"
4. Clique em "Redeploy" ou "Trigger Deployment"
5. Aguarde build terminar (~3-5 minutos)
6. Status deve estar "Successful" (verde)

---

## ✅ Passo 4: Testar Autenticação

1. Abra nova aba do navegador
2. Acesse: **https://gerajson.sensebike.com.br**
3. Resultado esperado:
   - Navegador pede usuário/senha
   - Caixa de diálogo aparece

4. Digite:
   - Username: **marco**
   - Password: **SenhaForte123!Marcos**
   - Clique OK

5. ✅ Aplicação carrega! 🔒

---

## 🎯 Vantagens Deste Método

- ✅ Tudo em código (no Dockerfile)
- ✅ Versionado no GitHub
- ✅ Automático (redeploy aplica tudo)
- ✅ Sem interface confusa do Coolify
- ✅ Fácil de mudar depois
- ✅ Funciona com qualquer versão do Coolify

---

## 🆘 Se Não Funcionar

### Problema 1: "Ainda não pede senha"

**Solução:**
1. Verifique se redeploy terminou (status verde)
2. Limpe cache do navegador: Ctrl+Shift+Delete
3. Feche navegador completamente
4. Abra nova aba
5. Acesse URL novamente

### Problema 2: "Erro 500 ou 503"

**Solução:**
1. Verifique logs no Coolify (Deployments → Logs)
2. Procure por erro de Nginx
3. Se houver erro de syntax no Dockerfile:
   - Corrija o erro
   - Commite novamente
   - Redeploy
4. Se persistir, volte a usar método via UI

### Problema 3: "Arquivo .htpasswd não encontrado"

**Solução:**
1. Verifique se `.htpasswd` está no repositório:
   ```bash
   git ls-files | grep htpasswd
   ```
2. Se não estiver, faça:
   ```bash
   git add .htpasswd
   git commit -m "chore: Adicionar .htpasswd"
   git push
   ```
3. Redeploy novamente

---

## 📊 Comparação de Métodos

| Método | Facilidade | Funciona | Quando Usar |
|--------|-----------|----------|------------|
| UI Coolify | ⭐⭐⭐⭐⭐ Fácil | ✅ | Se encontrar opção |
| Dockerfile | ⭐⭐⭐⭐ Médio | ✅ | Se UI não funcionar |
| Script Python | ⭐⭐⭐ Médio | ✅ | Para gerar .htpasswd |

---

## 🔐 Adicionar Mais Usuários

Se precisar adicionar usuário (ex: joao):

### Método 1: Usar Script Python
```bash
python gerar_htpasswd.py
# Segue o menu
# Gera novo .htpasswd com todos os usuários
```

### Método 2: Editar Manualmente

Adicione linha ao `.htpasswd`:
```
marco:$apr1$rnKr0o4a$EiOAVbQDUPYqBhLqrJL7b/
joao:$apr1$xyz...  ← NOVO USUÁRIO
```

### Depois:
```bash
git add .htpasswd
git commit -m "chore: Adicionar usuario joao"
git push
```

Redeploy automático vai aplicar!

---

## 📋 Checklist

- [ ] Editou Dockerfile
- [ ] Adicionou linha: `COPY .htpasswd /app/.htpasswd`
- [ ] Verificou sintaxe do Dockerfile
- [ ] Committou para GitHub
- [ ] Fez push para main
- [ ] Redeploy no Coolify iniciou
- [ ] Status ficou "Successful" (verde)
- [ ] Testou acesso em https://gerajson.sensebike.com.br
- [ ] Navegador pediu senha
- [ ] Logou com marco / SenhaForte123!Marcos
- [ ] Aplicação carregou

**Quando todos estiverem marcados: ✅ SUCESSO!**

---

## 💡 Dicas Finais

### Dica 1: Verificar Logs
Se houver erro, vá para Coolify → Logs:
```bash
# Procure por linhas como:
"Auth configured"
"Nginx started"
"Streamlit running"
```

### Dica 2: Testar Localmente (Opcional)
Se tiver Docker instalado:
```bash
docker build -t gerador-json .
docker run -p 8501:8501 gerador-json
```

### Dica 3: Outras Opções Nginx
Se quiser configurações mais avançadas:
- Rate limiting
- CORS
- Headers customizados
- etc.

Edite o bloco RUN do Dockerfile!

---

## 🎉 Próximo Passo

1. **Edite o Dockerfile** (adicione 2 linhas)
2. **Commite para GitHub**
3. **Redeploy no Coolify**
4. **Teste acesso** (deve pedir senha)

**Sua app estará protegida em ~5-8 minutos!** 🔒

---

## 🚀 Comece AGORA!

```bash
# 1. Edite Dockerfile (adicione após COPY .streamlit/)
COPY .htpasswd /app/.htpasswd

# 2. Commite
git add Dockerfile
git commit -m "chore: Adicionar auth via Dockerfile"
git push

# 3. Redeploy no Coolify (automático)

# 4. Teste em https://gerajson.sensebike.com.br
# 5. Digite: marco / SenhaForte123!Marcos
# 6. ✅ Pronto!
```

**Sucesso! 🔐✨**

