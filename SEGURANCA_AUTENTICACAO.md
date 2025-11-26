# 🔒 Segurança e Autenticação para Aplicações em Produção

## 📋 Visão Geral das Opções

Existem **4 camadas** de segurança que você pode implementar:

| Camada | Método | Dificuldade | Segurança | Recomendação |
|--------|--------|------------|-----------|--------------|
| 1 | Senha Streamlit nativa | Muito Fácil | Básica | ✅ Mínimo |
| 2 | Nginx + Auth Básica | Fácil | Boa | ✅ Recomendado |
| 3 | OAuth2 (Google/GitHub) | Médio | Excelente | ⭐ Melhor |
| 4 | JWT Token | Difícil | Muito Forte | 🔐 Máximo |

---

## 🔐 OPÇÃO 1: Senha Nativa do Streamlit (MAIS FÁCIL)

### Implementação

**Criar arquivo `.streamlit/secrets.toml`:**

```toml
# Senhas dos usuários (bcrypt hash)
password = "seu_hash_bcrypt_aqui"

# Ou simples (menos seguro, apenas para teste)
# password = "sua_senha_aqui"
```

**Adicionar ao `app_streamlit.py` (linhas iniciais):**

```python
import streamlit as st
import hashlib

# Função para verificar senha
def check_password():
    def password_entered():
        if st.session_state["password"] == st.secrets.get("password", ""):
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input(
            "Senha de acesso:",
            type="password",
            on_change=password_entered,
            key="password",
        )
        return False
    elif not st.session_state["password_correct"]:
        st.error("❌ Senha incorreta!")
        return False
    else:
        return True

# Verificar antes de executar o app
if not check_password():
    st.stop()

# Resto da aplicação aqui...
st.write("Conteúdo protegido!")
```

### Vantagens
- ✅ Muito rápido de implementar (~5 minutos)
- ✅ Nenhuma dependência extra
- ✅ Funciona em qualquer lugar

### Desvantagens
- ❌ Apenas 1 senha (ou máximo alguns usuários)
- ❌ Não há controle granular
- ❌ Senha compartilhada (segurança média)

### Melhor Para
- Aplicações internas pequenas
- Prototipagem rápida
- Acesso pessoal

---

## 🌐 OPÇÃO 2: Nginx + Autenticação (RECOMENDADO)

### Por que é a melhor opção para você?

- ✅ Funciona com **múltiplos usuários**
- ✅ Suporte nativo do Coolify (via Nginx)
- ✅ Fácil de implementar
- ✅ Segurança forte
- ✅ Sem código extra na aplicação

### Implementação no Coolify

**Passo 1: Criar arquivo `.htpasswd`**

Use online ou terminal para gerar:
```bash
# Instalar (se não tiver):
# apt-get install apache2-utils

# Criar para 1º usuário:
htpasswd -c .htpasswd marco

# Adicionar mais usuários:
htpasswd .htpasswd joao
htpasswd .htpasswd maria
```

**Resultado:** Arquivo `.htpasswd` com usuários/senhas hash

**Passo 2: Commitar para GitHub**

```bash
git add .htpasswd
git commit -m "chore: Arquivo de autenticação Nginx"
git push
```

**Passo 3: Configurar no Coolify**

1. Em seu app, vá para "Configuration"
2. Procure por "Basic Authentication" ou "Nginx"
3. Cole o conteúdo do `.htpasswd`
4. **OU** faça upload do arquivo
5. Salve e redeploy

**Passo 4: Testar**

1. Acesse a URL
2. Navegador pedirá usuário/senha
3. Digite: `marco` / `senha_que_criou`
4. Pronto! 🔒

### Arquivo `.htpasswd` Exemplo

```
marco:$apr1$r31.....$HqJZimJQg123456789
joao:$apr1$k42.....$XyZ789qwerty123
maria:$apr1$m55.....$AbC456defgh789
```

### Vantagens
- ✅ Múltiplos usuários
- ✅ Protege toda a URL
- ✅ Funciona com Coolify nativamente
- ✅ Sem código extra
- ✅ Muito rápido (~5 minutos)

### Desvantagens
- ❌ Sem logout (navegador controla)
- ❌ Sem auditoria detalhada

### Melhor Para
- **Suas aplicações!** (múltiplos usuários, fácil)

---

## 🔑 OPÇÃO 3: OAuth2 com Google/GitHub (MELHOR)

### Implementação

**Passo 1: Instalar dependência**

```bash
pip install streamlit-oauth
```

**Passo 2: Configurar no GitHub/Google**

[Para GitHub OAuth]
1. GitHub → Settings → Developer settings → OAuth Apps
2. Create new OAuth App
3. Nome: "Gerador JSON Hybris"
4. Homepage URL: `https://gerajson.sensebike.com.br`
5. Authorization callback: `https://gerajson.sensebike.com.br`
6. Copiar: Client ID e Client Secret

**Passo 3: Adicionar ao `.streamlit/secrets.toml`**

```toml
[oauth]
client_id = "seu_github_client_id"
client_secret = "seu_github_client_secret"
```

**Passo 4: Adicionar ao `app_streamlit.py`**

```python
from streamlit_oauth import oauth_manager

# Configurar OAuth
oauth = oauth_manager(
    provider="github",
    client_id=st.secrets.oauth.client_id,
    client_secret=st.secrets.oauth.client_secret,
    redirect_uri="https://gerajson.sensebike.com.br"
)

# Verificar login
if not oauth.is_authenticated:
    st.write("### 🔑 Faça login com GitHub")
    oauth.do_oauth()
    st.stop()

# Obter dados do usuário
user = oauth.get_user()
st.write(f"Bem-vindo, {user['login']}!")

# Resto da aplicação...
```

### Vantagens
- ✅ Login com Google/GitHub (familiar)
- ✅ Sem senha para gerenciar
- ✅ Controle granular por usuário
- ✅ Auditoria automática (GitHub logs)
- ✅ Muito seguro (OAuth2 enterprise-grade)

### Desvantagens
- ❌ Requer dependência extra
- ❌ Um pouco mais complexo

### Melhor Para
- Aplicações para equipes
- Acesso por múltiplos usuários
- Quando auditoria é importante

---

## 🛡️ OPÇÃO 4: Firewall + IP Whitelist (COMPLEMENTAR)

### Implementação no Coolify

1. Vá para "Network" ou "Security"
2. Procure por "Firewall Rules"
3. Adicione: "Allow only IPs: xxx.xxx.xxx.xxx"
4. Bloqueia acesso de qualquer outro IP

### Vantagens
- ✅ Camada adicional de proteção
- ✅ Bloqueia IPs suspeitos
- ✅ Muito eficaz

### Desvantagens
- ❌ Funciona apenas se IPs forem fixos
- ❌ Difícil para usuários em home office

---

## 🎯 RECOMENDAÇÃO PARA VOCÊ

### Nível 1: IMEDIATO (Implementar AGORA)

**Use: Nginx Basic Authentication (OPÇÃO 2)**

Por quê?
- ✅ Mais fácil que OAuth
- ✅ Suporta múltiplos usuários
- ✅ Funciona perfeitamente com Coolify
- ✅ Não requer código extra
- ✅ Implementável em 10 minutos

**Como implementar:**
1. Gerar `.htpasswd` com usuários
2. Commitar para GitHub
3. Configurar no Coolify
4. Pronto! 🔒

### Nível 2: DEPOIS (Se necessário)

Combine com:
- ✅ Firewall + IP Whitelist (se IPs forem fixos)
- ✅ SSL/HTTPS (já deve estar ativado no Coolify)

### Nível 3: FUTURO (Se escalar)

Migrar para OAuth2 quando:
- Muitos usuários
- Auditoria é importante
- Integração com outros sistemas

---

## 🚀 PLANO DE AÇÃO - PRÓXIMOS 15 MINUTOS

### 1. Gerar `.htpasswd` (5 minutos)

**Online (sem instalar):**
- Acesse: https://www.htaccesstools.com/htpasswd-generator/
- Nome: marco
- Senha: [sua_senha_forte]
- Clique "Create .htpasswd File"
- Copie o resultado

**Ou no terminal (se tiver Apache):**
```bash
htpasswd -c .htpasswd marco
# Digita senha 2x
```

### 2. Adicionar Usuários (2 minutos)

```bash
# Arquivo .htpasswd final terá:
marco:$apr1$r31.....$HqJZimJQg123456789
joao:$apr1$k42.....$XyZ789qwerty123
maria:$apr1$m55.....$AbC456defgh789
```

### 3. Commitar e Push (3 minutos)

```bash
git add .htpasswd
git commit -m "chore: Adicionar autenticação Nginx"
git push origin main
```

### 4. Configurar Coolify (5 minutos)

1. Coolify → Seu App
2. Configuration → Nginx
3. Procure por "Basic Authentication"
4. Cole conteúdo .htpasswd
5. Salve e Redeploy

### 5. Testar (1 minuto)

1. Acesse https://gerajson.sensebike.com.br
2. Navegador pede senha
3. Digite marco / sua_senha
4. Pronto! 🔒

---

## 📋 Checklist de Segurança

### Agora (Obrigatório)
- [ ] Implementar Autenticação (Opção 2)
- [ ] Criar múltiplos usuários
- [ ] Testar acesso

### Depois (Recomendado)
- [ ] Ativar HTTPS (deve estar automático no Coolify)
- [ ] Configurar SSL/TLS
- [ ] Adicionar IP Whitelist (se possível)

### Futuro (Quando escalar)
- [ ] Migrar para OAuth2
- [ ] Implementar auditoria
- [ ] Logs de acesso

---

## 🔐 Dicas Importantes

### Senhas Fortes
- Mínimo 12 caracteres
- Misturar maiúsculas, minúsculas, números, símbolos
- Nunca compartilhar
- Mudar a cada 90 dias

### Arquivo `.htpasswd`
- ⚠️ **NUNCA** commitar senhas em plain text
- Sempre usar hash (htpasswd faz isso)
- Manter seguro (acesso limitado no GitHub)

### URLs Sensíveis
- Sempre usar HTTPS (ativar no Coolify)
- Nunca usar HTTP (inseguro)
- Certificado SSL (automático no Coolify)

---

## ⚠️ Segurança Adicional

### Outras Camadas Importantes

1. **Firewall**
   - Coolify tem firewall built-in
   - Configure em "Security"
   - Bloqueie portas desnecessárias

2. **Logs e Auditoria**
   - Monitore acessos
   - Procure por atividades suspeitas
   - Configure alertas

3. **Rate Limiting**
   - Limite requisições por IP
   - Previne força bruta
   - Coolify pode configurar

4. **Backup**
   - Backup diário dos dados
   - Teste restore periodicamente

---

## 📞 Resumo Rápido

| Pergunta | Resposta |
|----------|----------|
| O que fazer AGORA? | Nginx Auth (Opção 2) |
| Quanto tempo leva? | ~15 minutos |
| É difícil? | Não! Muito fácil |
| Preciso código? | Não, Coolify faz tudo |
| Quantos usuários? | Ilimitado! |
| Pode mudar depois? | Sim! Fácil migrar |

---

## 🎉 Próximo Passo

1. Decida qual opção (recomendo Opção 2)
2. Gere o `.htpasswd`
3. Commite para GitHub
4. Configure no Coolify
5. **Sua aplicação estará 100% protegida! 🔒**

**Tempo total: ~15 minutos**

Quer que eu ajude com qualquer passo específico?

