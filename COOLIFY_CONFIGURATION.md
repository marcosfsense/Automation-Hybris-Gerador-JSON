# Configuração do Coolify para Gerador JSON Hybris

## 📋 Resumo Executivo

Esta aplicação Streamlit requer **configuração mínima** no Coolify. A maioria das configurações já está definida no `Dockerfile` e `.streamlit/config.toml`.

---

## 🔧 Configurações Necessárias no Coolify

### 1️⃣ PORT EXPOSES (Portas Expostas)

**Porta necessária:**
- **8501** - Porta padrão do Streamlit (já configurada no Dockerfile)

**Como configurar:**
1. No Coolify, vá para seu aplicativo
2. Procure por "Port Expose" ou "Network"
3. Certifique-se de que a porta **8501** está exposta
4. Não é necessário mapear para outra porta (a menos que tenha conflito)

```
Port Internal: 8501
Port External: 8501 (ou qualquer porta que desejar)
```

---

### 2️⃣ ENVIRONMENT VARIABLES (Variáveis de Ambiente)

**Recomendado - Adicionar no Coolify:**

```env
# Streamlit Configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_LOGGER_LEVEL=info
STREAMLIT_CLIENT_TOOLBAR_MODE=minimal

# Python Configuration
PYTHONUNBUFFERED=1
PYTHONIOENCODING=utf-8

# Optional: Logging
STREAMLIT_LOGGER_LEVEL=info
```

**Por que PYTHONUNBUFFERED=1?**
- Garante que logs Python são exibidos em tempo real no Coolify
- Essencial para debug e monitoramento

**Como adicionar no Coolify:**
1. Vá para "Environment" ou "Variables"
2. Clique em "Add Variable"
3. Adicione cada linha acima
4. Salve e redeploy

---

### 3️⃣ PERSISTENT STORAGE (Armazenamento Persistente)

**Esta aplicação precisa de storage persistente?** NÃO

**Por quê?**
- Não há banco de dados
- Não há arquivos salvos que precisam persistir entre restarts
- Os JSONs são gerados em tempo real e baixados pelo usuário
- Streamlit cache é temporário

**Mas se você quiser logs persistentes:**

1. Crie um volume no Coolify:
   - **Path inside container:** `/app/logs`
   - **Storage size:** 1GB (mais que suficiente)

2. No Dockerfile, adicione (opcional):
   ```dockerfile
   RUN mkdir -p /app/logs
   ```

**Se NÃO precisa de logs persistentes: PULE esta etapa**

---

### 4️⃣ OUTRAS CONFIGURAÇÕES IMPORTANTES

#### A) Build Arguments (NÃO necessário)
- Deixe em branco
- O Dockerfile já está otimizado

#### B) Restart Policy (IMPORTANTE)
**Defina para: "Always" ou "Unless-stopped"**
- Garante que o app reinicia se cair
- Padrão recomendado para aplicações em produção

#### C) Deploy Strategy
- **Auto Deploy on Push:** ✅ **ATIVAR**
  - Coolify vai detectar push no GitHub e fazer deploy automático
  - Baseado no Dockerfile que enviamos

#### D) Health Check
**Já configurado no Dockerfile:**
```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3
```
- Coolify vai usar isso automaticamente
- Nenhuma configuração adicional necessária

---

## 🚀 Passo a Passo: Configurar no Coolify

### Passo 1: Conectar Repositório
1. Em Coolify, clique em "Create an Application"
2. Selecione "GitHub" como source
3. Selecione seu repositório: `marcosfsense/Automation-Hybris-Gerador-JSON`
4. Selecione branch: `main`

### Passo 2: Configurar Tipo de Deploy
1. **Build Pack:** Selecione "Docker"
2. Coolify vai detectar o `Dockerfile` automaticamente
3. Clique em "Next"

### Passo 3: Configurar Networking
1. **Port Expose:**
   - Internal Port: `8501`
   - External Port: `8501` (ou deixar que Coolify assign)

2. **Public URL:** Será gerado automaticamente (ex: `app.coolify.io` ou seu domínio)

### Passo 4: Configurar Environment Variables
1. Clique em "Add Environment Variable"
2. Adicione as variáveis recomendadas (ver seção 2️⃣ acima)
3. **Importante:** `PYTHONUNBUFFERED=1` é essencial

### Passo 5: Storage (Opcional)
- Se quer logs persistentes, configure um volume
- Path: `/app/logs`
- Size: `1GB`

### Passo 6: Auto Deploy (Recomendado)
1. Vá para "Deployments"
2. Ative "Auto Deploy on Push"
3. Escolha branch: `main`

### Passo 7: Deploy!
1. Clique em "Deploy"
2. Espere ~3-5 minutos para a primeira build
3. Você receberá uma URL pública (ex: `https://app-1234.coolify.io`)

---

## ✅ Checklist de Configuração

- [ ] Repository conectado ao Coolify
- [ ] Docker selecionado como Build Pack
- [ ] Porta 8501 exposta
- [ ] Environment Variables adicionadas:
  - [ ] `STREAMLIT_SERVER_PORT=8501`
  - [ ] `STREAMLIT_SERVER_ADDRESS=0.0.0.0`
  - [ ] `STREAMLIT_SERVER_HEADLESS=true`
  - [ ] `PYTHONUNBUFFERED=1`
- [ ] Restart Policy definido para "Always"
- [ ] Auto Deploy on Push ativado
- [ ] Primeira build completa com sucesso
- [ ] URL pública acessível
- [ ] Testa aplicação (cole um JSON de exemplo)
- [ ] Logs aparecem no Coolify (via PYTHONUNBUFFERED)

---

## 🔍 Como Debugar Problemas

### Problema: "Application fails to start"
**Solução:**
1. Verifique logs no Coolify
2. Procure por: `streamlit run src/app_streamlit.py`
3. Se houver erro de import, verifique `requirements.txt`
4. Adicione mais verbosidade: `STREAMLIT_LOGGER_LEVEL=debug`

### Problema: "Port already in use"
**Solução:**
1. Altere Port Expose para uma porta diferente (ex: 8502)
2. Coolify fará o mapeamento automaticamente

### Problema: "Application timeout on startup"
**Solução:**
1. Aumentar `start-period` no HEALTHCHECK (já em 5s, está bom)
2. Verificar se há muitos imports lentosos
3. Adicionar mais RAM alocado no Coolify

### Problema: "Cannot access from external URL"
**Solução:**
1. Verifique se `STREAMLIT_SERVER_ADDRESS=0.0.0.0` está configurado
2. Certifique-se de que proxy está habilitado no Coolify
3. Aguarde 2-3 minutos após deploy (DNS pode levar tempo)

---

## 📊 Monitoramento Recomendado

### Logs
- **Acesse em:** Coolify → Seu App → Logs
- **Procure por:** "Streamlit app is running"
- **Frequência:** Verifique após cada deploy

### Health Status
- **Verifique:** Status do container no Coolify
- **Esperado:** "Healthy" (verde)
- **Se "Unhealthy":** Verifique logs

### CPU/Memória
- **Monitor:** Consumo durante uso
- **Esperado:** ~100-200MB de RAM (mínimo)
- **Pico:** Pode subir a ~300-400MB com múltiplos usuários

---

## 🎯 Recomendações Finais

1. **Não é necessário:**
   - Persistent Storage (a menos que queira logs)
   - Custom environment variables (apenas os recomendados)
   - Custom domains (use o padrão do Coolify inicialmente)

2. **Ative:**
   - Auto Deploy on Push (automação FTW!)
   - Email notifications (para alertas de deploy)
   - Health checks (já configurado)

3. **Teste:**
   - Após deploy, cole um JSON de teste
   - Verifique se a saída é gerada corretamente
   - Teste o download do JSON

---

## 🔗 Referências Rápidas

- **Dockerfile:** Já otimizado, sem mudanças necessárias
- **Config.toml:** Já configurado para produção
- **Requirements.txt:** Apenas Streamlit necessário
- **GitHub:** Push automático dispara deploy no Coolify

**Você está pronto para fazer deploy! 🎉**
