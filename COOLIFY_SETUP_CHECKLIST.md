# ✅ Checklist Setup Coolify - Gerador JSON Hybris

## 📋 Checklist Rápido (5-10 minutos)

### FASE 1: Preparação GitHub ✅ (JÁ FEITO)
- [x] Dockerfile criado e commitado
- [x] .streamlit/config.toml criado e commitado
- [x] .dockerignore criado e commitado
- [x] .gitignore atualizado para permitir config.toml
- [x] Push para GitHub concluído
- [x] Branch main atualizado

**Status:** ✅ COMPLETO - Pronto para conectar ao Coolify

---

## FASE 2: Configurar Coolify (FAZER AGORA)

### 2.1 Conectar Repositório GitHub
- [ ] Abra Coolify no seu navegador
- [ ] Clique em "Create an Application" ou "New Service"
- [ ] Selecione "GitHub" como source
- [ ] Autorize o acesso ao seu GitHub (se não autorizado ainda)
- [ ] Selecione o repositório: `marcosfsense/Automation-Hybris-Gerador-JSON`
- [ ] Selecione o branch: `main`

**Esperado:** Coolify detecta o Dockerfile automaticamente

### 2.2 Selecionar Tipo de Deploy
- [ ] Em "Build Pack" selecione: **Docker**
- [ ] Clique "Next" ou "Continue"

**Esperado:** Coolify vai usar o Dockerfile do repositório

### 2.3 Configurar Port Expose
- [ ] **Internal Port:** `8501`
- [ ] **External Port:** `8501` (ou deixar Coolify atribuir)
- [ ] Salve esta configuração

**Esperado:** Porta 8501 ativa após deploy

### 2.4 Adicionar Environment Variables
Complete esta seção com **cuidado**:

- [ ] Clique em "Add Variable" ou "Environment"

Para cada linha abaixo, clique "Add Variable" e preencha:

#### OBRIGATÓRIO (4 variáveis):
```
1. STREAMLIT_SERVER_PORT = 8501
2. STREAMLIT_SERVER_ADDRESS = 0.0.0.0
3. STREAMLIT_SERVER_HEADLESS = true
4. PYTHONUNBUFFERED = 1
```

- [ ] Variável 1 adicionada
- [ ] Variável 2 adicionada
- [ ] Variável 3 adicionada
- [ ] Variável 4 adicionada

#### RECOMENDADO (4 variáveis extras):
```
5. STREAMLIT_LOGGER_LEVEL = info
6. STREAMLIT_CLIENT_TOOLBAR_MODE = minimal
7. STREAMLIT_CLIENT_SHOW_ERROR_DETAILS = false
8. PYTHONIOENCODING = utf-8
```

- [ ] Variável 5 adicionada (opcional)
- [ ] Variável 6 adicionada (opcional)
- [ ] Variável 7 adicionada (opcional)
- [ ] Variável 8 adicionada (opcional)

### 2.5 Configurar Restart Policy
- [ ] Procure por "Restart Policy"
- [ ] Selecione: **Always** ou **Unless-stopped**

**Esperado:** App reinicia se cair

### 2.6 Ativar Auto Deploy (Opcional mas Recomendado)
- [ ] Procure por "Auto Deploy" ou "Deployments"
- [ ] Ative: "Deploy on push"
- [ ] Selecione branch: `main`

**Benefício:** Qualquer push no GitHub dispara deploy automático

### 2.7 Storage/Volumes (NÃO NECESSÁRIO)
- [ ] Deixe como padrão (sem volumes persistentes)

**Justificativa:** App não usa banco de dados, tudo é em memória

---

## FASE 3: Deploy Inicial

### 3.1 Iniciar Deploy
- [ ] Clique em "Deploy" ou "Save & Deploy"
- [ ] Aguarde a build terminar (3-5 minutos primeira vez)

**Status esperado:** ✅ Deployment successful

### 3.2 Verificar Logs
- [ ] Clique na aba "Logs"
- [ ] Procure por: `Streamlit app is running`
- [ ] Procure por: `Ready to accept connections`
- [ ] Certifique-se de que NÃO há `ERROR` ou `CRITICAL`

**Esperado:** Logs verdes, sem erros

### 3.3 Acessar Aplicação
- [ ] Copie a URL pública gerada (ex: `https://app-1234.coolify.io`)
- [ ] Cole a URL no navegador
- [ ] Aguarde a página carregar (primeira vez pode levar 10-30s)

**Esperado:** Página do Gerador JSON Hybris carrega

---

## FASE 4: Testar Funcionalidade

### 4.1 Teste Básico
- [ ] Na aplicação, vá para a Seção 1
- [ ] Cole um JSON de teste mínimo:
```json
{
  "id": "test-123",
  "items": [],
  "price": 10000,
  "number": "TEST001",
  "status": "PAID",
  "created_at": "2024-11-26T10:00:00Z",
  "updated_at": "2024-11-26T10:00:00Z",
```

- [ ] Seção 2: Selecione "PIX"
- [ ] Seção 2.5: Preenchido com "Fake callback - "
- [ ] Seção 3: Preencha o formulário PIX
- [ ] Clique em "Gerar JSON"
- [ ] Resultado deve aparecer (sem erros)

**Esperado:** JSON gerado com sucesso

### 4.2 Teste de Download
- [ ] Clique em "Copiar para Clipboard" ou "Download"
- [ ] Verifique se JSON foi copiado/baixado

**Esperado:** JSON disponível para copiar/baixar

---

## FASE 5: Verificações Finais

### 5.1 Health Status
- [ ] Volte para Coolify
- [ ] Verifique o status do container: deve estar **"Healthy"** (verde)

**Esperado:** Status verde ✅

### 5.2 Auto Restart
- [ ] No Coolify, procure por opção de "Restart"
- [ ] Clique em "Restart"
- [ ] Aguarde ~30 segundos
- [ ] Acesse a URL pública novamente

**Esperado:** Aplicação volta online rapidamente

### 5.3 Monitoramento
- [ ] Monitore CPU/Memória (deve estar baixo: ~100-200MB)
- [ ] Monitore Logs periodicamente

**Esperado:** Consumo baixo, logs limpos

---

## ⚡ Quick Reference - Portas e URLs

```
Porta Interna: 8501 (dentro do container)
Porta Externa: 8501 (que você acessa externamente)

URL Pública: https://[seu-app].coolify.io
             ou seu domínio customizado

Health Check: Automático a cada 30s
Status: Verde = OK, Amarelo = Verificando, Vermelho = Erro
```

---

## 🆘 Troubleshooting Rápido

### ❌ "Application fails to start"
1. Verifique logs no Coolify
2. Procure por erro de Python
3. **Solução:** Verifique se `PYTHONUNBUFFERED=1` foi adicionado
4. Redeploy

### ❌ "Cannot access the application"
1. Aguarde 2-3 minutos (DNS/proxy pode levar tempo)
2. Verifique se Port 8501 está no "Port Expose"
3. **Solução:** Verifique se `STREAMLIT_SERVER_ADDRESS=0.0.0.0` foi adicionado
4. Redeploy

### ❌ "Timeout when accessing"
1. Verifique se aplicação iniciou (logs: "Streamlit app is running")
2. Verifique consumo de CPU/memória
3. **Solução:** Pode levar tempo na primeira inicialização
4. Aguarde mais 30 segundos

### ❌ "Port already in use"
1. Mude a porta externa para 8502, 8503, etc
2. Coolify fará o mapeamento automaticamente
3. Redeploy

---

## ✨ Próximos Passos (Após Sucesso)

1. **Domínio Customizado (Opcional)**
   - Aponte seu domínio para Coolify
   - Aplique SSL/TLS automaticamente

2. **Monitoramento**
   - Configure alertas de email
   - Monitorar health status

3. **Backups (se necessário)**
   - Configure backup automático do repositório
   - Não é necessário para esta app

4. **Scaling (se necessário)**
   - Aumente memória/CPU no Coolify
   - Coolify suporta auto-scaling

---

## 📞 Suporte Rápido

Se algo der errado:

1. **Verifique os Logs** (Coolify → Logs)
2. **Verifique as Variáveis** (Coolify → Variables)
3. **Verifique a Porta** (Coolify → Port Expose)
4. **Teste Localmente** (Execute `streamlit run src/app_streamlit.py`)
5. **Redeploy** (Force rebuild no Coolify)

---

## 🎉 Status Final

Quando tudo estiver verde:

- [x] Código em GitHub
- [x] Coolify conectado
- [x] Docker build bem-sucedido
- [x] Aplicação online
- [x] Porta acessível
- [x] Funcionalidade testada
- [x] Health check OK
- [x] Logs limpos
- [x] Auto deploy ativo

**Você está pronto! 🚀**

Agora você pode:
- Compartilhar a URL com usuários
- Fazer push de mudanças (deploy automático)
- Monitorar aplicação via Coolify
- Escalar recursos conforme necessário

