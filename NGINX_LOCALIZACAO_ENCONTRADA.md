# 🎯 Localizando Nginx no Coolify - Guia Baseado na Sua Tela

## ✅ Tela Atual Identificada

Você está em: **Configuration → General**

Vejo o menu lateral esquerdo com várias opções. Vamos procurar a opção correta!

---

## 🔍 Onde Procurar (Baseado na Tela)

### Menu Lateral Esquerdo Visible:

Você deve ver estas opções (rol para baixo se precisar):

```
┌─────────────────────────────┐
│ Configuration               │
│ ├─ General ✓ (você está aqui)
│ ├─ Advanced
│ ├─ Environment Variables
│ ├─ Persistent Storage
│ ├─ Git Source
│ ├─ Servers
│ ├─ Scheduled Tasks
│ ├─ Webhooks
│ ├─ Preview Deployments
│ ├─ Healthcheck
│ ├─ Rollback
│ ├─ Resource Limits
│ ├─ Resource Operations
│ ├─ Metrics
│ ├─ Tags
│ └─ Danger Zone ← ROL PARA BAIXO
└─────────────────────────────┘
```

---

## 🎯 OPÇÃO 1: Procurar em "Advanced"

### Passo 1:
Clique em **"Advanced"** no menu lateral esquerdo

### Passo 2:
Procure por campos com nomes:
- [ ] "Nginx Configuration"
- [ ] "Nginx Custom Config"
- [ ] "Web Server Config"
- [ ] "Proxy Config"

### Se encontrar:
- Campo de texto grande aparecerá
- Cole o .htpasswd ali
- Clique Save

---

## 🎯 OPÇÃO 2: Procurar em "Servers"

### Passo 1:
Clique em **"Servers"** no menu lateral esquerdo

### Passo 2:
Procure por:
- [ ] "Nginx"
- [ ] "Reverse Proxy"
- [ ] "Load Balancer"
- [ ] "Configuration"

### Se encontrar:
- Cole o .htpasswd
- Clique Save

---

## 🎯 OPÇÃO 3: Procurar em "Healthcheck"

Sim, às vezes autenticação fica próximo a Healthcheck!

### Passo 1:
Clique em **"Healthcheck"** no menu lateral esquerdo

### Passo 2:
Procure por:
- [ ] "Authentication"
- [ ] "Basic Auth"
- [ ] "Nginx"

---

## 🎯 OPÇÃO 4: Procurar Abas no Topo

Você vê estas abas no topo?
```
[Configuration] [Deployments] [Logs] [Terminal] [Links] [Advanced]
```

### Se sim:
Clique em **"Advanced"** (abas no topo)

---

## 🎯 OPÇÃO 5: Procurar em "Danger Zone"

Às vezes fica em configurações "avançadas/perigosas":

### Passo 1:
**ROL PARA BAIXO** no menu lateral esquerdo

### Passo 2:
Clique em **"Danger Zone"**

### Passo 3:
Procure por "Nginx" ou "Authentication"

---

## 📋 Checklist - Siga na Ordem

- [ ] 1. Clique em **"Advanced"** (menu lateral)
      - Procure "Nginx Configuration"
      - Se encontrar, STOP aqui! ✅

- [ ] 2. Se não encontrar, clique em **"Servers"**
      - Procure "Nginx" ou "Reverse Proxy"
      - Se encontrar, STOP aqui! ✅

- [ ] 3. Se não encontrar, clique em **"Healthcheck"**
      - Procure "Authentication"
      - Se encontrar, STOP aqui! ✅

- [ ] 4. Se não encontrar, procure abas no topo
      - Clique "Advanced" nas abas
      - Se encontrar, STOP aqui! ✅

- [ ] 5. Se nada acima funcionou...
      - ROL PARA BAIXO no menu lateral
      - Clique "Danger Zone"
      - Procure "Nginx"
      - Se encontrar, STOP aqui! ✅

---

## 🆘 Se Ainda Não Encontrar Depois de Tudo

### Alternativa A: Use Dockerfile (GARANTIDO)

Você não precisa encontrar Nginx! Use:

**`CONFIGURAR_NGINX_VIA_DOCKERFILE.md`**

Passos:
1. Edite `Dockerfile` (apenas 1 linha)
2. Commite para GitHub
3. Redeploy
4. Pronto! 🔐

---

### Alternativa B: Procure por "Proxy" ou "Reverse"

Às vezes Nginx é chamado de:
- "Reverse Proxy"
- "Web Server"
- "Load Balancer"
- "HTTP Config"
- "Port Configuration"

---

## 📸 Visual - O Que Procurar

Quando encontrar a opção correta, você verá algo assim:

### ✅ Se for Campo de Texto:
```
Nginx Configuration
┌─────────────────────────────┐
│ location / {                │
│     proxy_pass http://...   │
│ }                           │
│                             │
│ Cole aqui o .htpasswd       │
└─────────────────────────────┘
```

### ✅ Se for Toggle:
```
□ Enable Nginx Authentication
  Username: [________]
  Password: [________]
  (Cole .htpasswd aqui)
```

### ✅ Se for Campo Simples:
```
Basic Authentication Credentials:
[marco:$apr1$rnKr0o4a$EiOAVbQDUPYqBhLqrJL7b/]
```

---

## 🎯 Próximos Passos

### AGORA:
1. Siga o checklist acima (5 opções)
2. Clique em CADA opção do menu lateral
3. Procure por "Nginx", "Auth", ou "Proxy"
4. Quando encontrar → **AVISE-ME!**

### EU VOU:
1. Dar instruções EXATAS para colar o .htpasswd
2. Configurar e fazer redeploy
3. Testar acesso

---

## 💡 Dica Extra: Use Ctrl+F

Se o menu for muito grande:

**Windows/Linux:**
- Pressione: **Ctrl+F**
- Procure: "nginx"
- Ou procure: "auth"

**Mac:**
- Pressione: **Cmd+F**
- Procure: "nginx"

---

## 📞 Resumo Rápido

| Clique em | Procure por | Se encontrar |
|-----------|-------------|--------------|
| Advanced | Nginx Configuration | Cole .htpasswd |
| Servers | Reverse Proxy / Nginx | Cole .htpasswd |
| Healthcheck | Authentication | Cole .htpasswd |
| Abas no topo | Advanced | Procure Nginx |
| Danger Zone | Nginx / Proxy | Cole .htpasswd |

---

## 🚀 Comece AGORA!

1. **Clique em "Advanced"** (no menu lateral)
2. **Procure por "Nginx"**
3. **Quando encontrar → AVISE-ME!**

Eu vou guiar o resto! 👍

**Encontrou? Me avisa qual é a opção!** 🎯

