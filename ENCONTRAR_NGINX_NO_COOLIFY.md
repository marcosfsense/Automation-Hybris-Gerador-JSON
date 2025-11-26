# 🔍 Como Encontrar a Opção Nginx/Auth no Coolify

## 📍 Locais Onde Pode Estar

### LOCAL 1: Em "Configuration"

**Caminho:**
1. Seu app: Gerador-JSON-Hybris
2. Clique em **"Configuration"**
3. Procure por:
   - [ ] "Nginx"
   - [ ] "Advanced"
   - [ ] "Web Server"
   - [ ] "Reverse Proxy"

**Se encontrar "Nginx Config":**
- Será um campo de texto grande
- Cole o .htpasswd ali

---

### LOCAL 2: Em "Settings" ou "Advanced Settings"

**Caminho:**
1. Seu app: Gerador-JSON-Hybris
2. Clique em **"Settings"** ou **"More"**
3. Procure por:
   - [ ] "Advanced Settings"
   - [ ] "Security"
   - [ ] "Authentication"
   - [ ] "Basic Auth"

---

### LOCAL 3: Em "Network" ou "Security"

**Caminho:**
1. Seu app: Gerador-JSON-Hybris
2. Clique em **"Network"** ou **"Security"**
3. Procure por:
   - [ ] "Authentication"
   - [ ] "Basic Auth"
   - [ ] "Proxy"
   - [ ] "Nginx"

---

### LOCAL 4: No Menu Principal Lateral

**Caminho:**
1. No lado esquerdo do Coolify
2. Procure por menu com:
   - [ ] "Applications"
   - [ ] "Services"
   - [ ] "Deployments"
   - [ ] "Settings"

3. Clique no seu app
4. Procure abas no topo:
   - [ ] "Overview"
   - [ ] "Deployments"
   - [ ] "Configuration"
   - [ ] "Logs"
   - [ ] "Network" ← PODE ESTAR AQUI

---

## 🎯 Passo a Passo Visual

### Se Você Vê Esta Tela:

```
┌─────────────────────────────────────────┐
│ Gerador-JSON-Hybris                     │
│                                         │
│ [Overview] [Deployments] [Logs]         │
│ [Configuration] [Network] [...]         │
└─────────────────────────────────────────┘
```

**Clique em "Configuration"** e procure por "Nginx"

---

### Se Você Vê Esta Tela:

```
┌─────────────────────────────────────────┐
│ Seu App Settings                        │
│                                         │
│ [General]                               │
│ [Environment]                           │
│ [Build]                                 │
│ [Advanced] ← CLIQUE AQUI                │
│ [Security]                              │
└─────────────────────────────────────────┘
```

**Clique em "Advanced"** e procure por "Nginx"

---

## 🔎 O Que Procurar

Quando encontrar a opção correta, você verá:

### ✅ Campo de Texto Grande
```
Nginx Configuration
┌──────────────────────────┐
│ location / {             │
│   proxy_pass ...         │
│   ...                    │
│ }                        │
└──────────────────────────┘

Cole aqui: marco:$apr1$rnKr0o4a$EiOAVbQDUPYqBhLqrJL7b/
```

### ✅ Campo Simples
```
Basic Authentication
┌──────────────────────────┐
│ [Toggle] Enable          │
│ Username: [____]         │
│ Password: [____]         │
└──────────────────────────┘
```

### ✅ Opção de Upload
```
Upload .htpasswd File
┌──────────────────────────┐
│ [Choose File]            │
│ Select .htpasswd from    │
│ your computer            │
└──────────────────────────┘
```

---

## 📋 Checklist de Procura

Marque conforme procura:

- [ ] Abriu seu app no Coolify
- [ ] Procurou em "Configuration"
- [ ] Procurou em "Advanced Settings"
- [ ] Procurou em "Network"
- [ ] Procurou em "Security"
- [ ] Procurou em "Settings"
- [ ] Procurou em "More Options"
- [ ] Procurou em menu lateral esquerdo
- [ ] Procurou em abas no topo
- [ ] Encontrou algo com "Nginx" ou "Auth"

**Se marcar tudo e não encontrar:** Vá para a seção "Alternativa" abaixo

---

## 🆘 Se Ainda Não Encontrar

### Alternativa 1: Configurar via Dockerfile

Se Coolify não tem interface para Nginx Auth, você pode configurar direto no Dockerfile:

**Edite o `Dockerfile`** e adicione depois da linha `COPY .streamlit/`:

```dockerfile
# Copiar arquivo .htpasswd
COPY .htpasswd /app/.htpasswd

# Instalar htpasswd tools (opcional)
RUN apt-get update && apt-get install -y apache2-utils && rm -rf /var/lib/apt/lists/*
```

Depois:
1. Commit para GitHub
2. Redeploy no Coolify
3. Nginx usará o arquivo .htpasswd automaticamente

---

### Alternativa 2: Procurar em "Logs" ou "Terminal"

Se Coolify tem acesso a terminal:

1. Vá para "Terminal" (se existir)
2. Execute:
```bash
cat /app/.htpasswd
```

Se este arquivo existir, significa que Nginx já consegue ler!

---

### Alternativa 3: Contatar Suporte Coolify

Se ainda não conseguir:
1. Vá para ajuda do Coolify (menu)
2. Procure por "Documentation"
3. Procure por "Nginx" ou "Authentication"
4. Ou envie ticket de suporte

---

## 💡 Dicas Práticas

### Dica 1: Use Atalhos do Navegador
```
Ctrl+F ou Cmd+F
Procure por: "nginx"
Procure por: "auth"
Procure por: "basic"
```

### Dica 2: Explore Menus
Clique em **CADA** opção/abas que vir:
- Overview
- Deployments
- Logs
- Configuration
- Network
- Security
- Advanced
- More
- Settings
- etc.

### Dica 3: Procure por Palavras-Chave
Procure por:
- "nginx"
- "auth"
- "basic"
- "proxy"
- "htpasswd"
- "authentication"

---

## 📸 Estrutura Típica do Coolify

```
Dashboard
├── Servers
├── Projects
│   └── Seu Projeto
│       └── Gerador-JSON-Hybris
│           ├── Overview
│           ├── Deployments
│           ├── Logs
│           ├── Configuration  ← PROCURE AQUI
│           ├── Network        ← OU AQUI
│           ├── Security       ← OU AQUI
│           └── More...
└── Settings
```

---

## 🎯 Próximo Passo

1. **Abra seu Coolify**
2. **Vá para seu app**
3. **Procure nas seguintes abas (nesta ordem):**
   1. Configuration
   2. Advanced Settings
   3. Network
   4. Security
   5. Settings
   6. More Options

4. **Procure por "Nginx" ou "Auth"**

5. **Quando encontrar:**
   - Cole o .htpasswd
   - Salve
   - Redeploy

6. **Se não encontrar em nenhum lugar:**
   - Use Alternativa 1 (Dockerfile)
   - Ou contate suporte Coolify

---

## 📞 Resumo

| Se vê... | Então... |
|----------|----------|
| "Configuration" | Clique e procure Nginx |
| "Advanced" | Clique e procure Auth |
| "Network" | Clique e procure Security |
| "Security" | Procure Authentication |
| Nada disso | Use Dockerfile (Alternativa 1) |

---

## 🚀 Comece Procurando AGORA!

1. Abra Coolify
2. Vá para seu app
3. Clique em **"Configuration"**
4. Use Ctrl+F para procurar "nginx"
5. **Avise quando encontrar!** 👍

Quando encontrar, volta aqui e sigo com próximos passos!

