# ⚡ Setup Autenticação Rápido (15 minutos)

## 🎯 Objetivo
Proteger sua aplicação `gerajson.sensebike.com.br` com autenticação de usuários.

---

## 🚀 Opção Recomendada: Nginx Basic Auth

### Por que?
- ✅ Mais rápido (15 min)
- ✅ Nenhum código extra
- ✅ Múltiplos usuários
- ✅ Nativo no Coolify

---

## 📋 Passo 1: Gerar Arquivo `.htpasswd`

### Método 1: Online (SEM instalar nada)

1. Abra: https://www.htaccesstools.com/htpasswd-generator/

2. Preencha para **CADA usuário**:
   - **Username:** marco
   - **Password:** SenhaForte123!
   - Clique "Create .htpasswd File"

3. Copie o resultado

### Método 2: Terminal (Se tiver)

```bash
# Instalar (Ubuntu/Debian):
sudo apt-get install apache2-utils

# Criar arquivo (primeiro usuário):
htpasswd -c .htpasswd marco
# Digita senha 2x

# Adicionar mais usuários:
htpasswd .htpasswd joao
htpasswd .htpasswd maria
```

---

## 📄 Resultado Esperado

O arquivo `.htpasswd` ficará assim:

```
marco:$apr1$r31...$HqJZimJQg123456789abcdef
joao:$apr1$k42...$XyZ789qwerty123456
maria:$apr1$m55...$AbC456defghijk789
```

**Importante:** É um hash! Não é a senha em plain text.

---

## 💾 Passo 2: Criar Arquivo no Projeto

1. Abra seu editor (VS Code)
2. Crie novo arquivo: `.htpasswd`
3. Cole o conteúdo do passo anterior
4. Salve

---

## 🔄 Passo 3: Commitar para GitHub

```bash
# No terminal, no diretório do projeto:
cd "c:\Users\marcos.fernandes\Desktop\AUTOMAÇÃO HYBRIS - GERADOR DE JSONs"

# Adicionar arquivo
git add .htpasswd

# Commitar
git commit -m "chore: Adicionar autenticação Nginx (.htpasswd)"

# Push
git push origin main
```

---

## ⚙️ Passo 4: Configurar no Coolify (Mais Importante)

### LOCAL: Coolify Web Interface

1. **Abra seu Coolify** no navegador
2. **Vá para seu app:** Gerador-JSON-Hybris
3. **Clique em "Configuration"** (ou "Settings")
4. **Procure por "Nginx"** ou "Basic Authentication"

### Se encontrar "Nginx Config":
```
- Procure pela seção [basicauth] ou [auth]
- Cole o conteúdo do .htpasswd ali
```

### Se encontrar "Basic Authentication" direto:
```
- Procure por campo "Upload" ou "Paste"
- Cole o conteúdo do .htpasswd
```

### Se não encontrar:
```
Procure em:
- "Advanced" → "Nginx"
- "Network" → "Authentication"
- "Security" → "Basic Auth"
```

### Depois de Colar:
1. Clique **"Save"**
2. Clique **"Redeploy"** ou **"Restart"**
3. Aguarde alguns segundos

---

## ✅ Passo 5: Testar Acesso

1. **Abra nova aba/janela do navegador**
2. **Digite:** https://gerajson.sensebike.com.br
3. **Resultado esperado:**
   - Navegador pede usuário/senha
   - Caixa de diálogo aparece

4. **Digite:**
   - Username: marco
   - Password: [sua_senha]
   - Clique OK

5. **Pronto!** Aplicação carrega com sucesso 🔒

---

## 🆘 Se Não Funcionar

### Problema 1: "Não vejo opção de Basic Auth no Coolify"

**Solução:**
1. Verifique versão do Coolify (menu no canto)
2. Atualize se estiver desatualizado
3. Procure em "Advanced Settings"
4. Ou configure via arquivo `.htpasswd` no Dockerfile

### Problema 2: "Diz senha incorreta, mas está certa"

**Solução:**
1. Certifique-se que `.htpasswd` foi committado
2. Aguarde redeploy completar (green status)
3. Limpe cache do navegador (Ctrl+Shift+Delete)
4. Tente nova aba (abre nova conexão)

### Problema 3: "Não dá opção de senha"

**Solução:**
1. Verifique se redeploy terminou
2. Verifique se arquivo `.htpasswd` existe
3. Reinicie a aplicação no Coolify
4. Aguarde alguns segundos

---

## 📊 Resultado Final

Depois que configurar:

```
❌ Antes:
   Qualquer um acessa: https://gerajson.sensebike.com.br

✅ Depois:
   Pede usuário/senha ANTES de entrar
   Apenas autorizados têm acesso
```

---

## 🔐 Adicionar Mais Usuários

Quando precisar adicionar novo usuário:

1. **Regenerar `.htpasswd`** com novo usuário
2. **Commitar** para GitHub
3. **Redeploy** no Coolify

Exemplo: Adicionar "ana"

```
marco:$apr1$r31...$HqJZimJQg123456789abcdef
joao:$apr1$k42...$XyZ789qwerty123456
maria:$apr1$m55...$AbC456defghijk789
ana:$apr1$n77...$DeF890klmnop234567        ← NOVO
```

---

## 🔄 Mudar Senha de um Usuário

1. Regenerar `.htpasswd` com nova senha
2. Commitar e push
3. Redeploy

Simples assim!

---

## 📋 Checklist

- [ ] Gerou arquivo `.htpasswd`
- [ ] Criou arquivo no projeto
- [ ] Committou para GitHub
- [ ] Configurou no Coolify
- [ ] Fez redeploy
- [ ] Testou acesso (pediu senha)
- [ ] Logou com sucesso
- [ ] Aplicação carregou

**Quando todos estiverem marcados: ✅ SEGURO!**

---

## ⏱️ Timeline

```
Agora      Gera .htpasswd (5 min)
   ↓
+5 min     Commita para GitHub (2 min)
   ↓
+7 min     Configura no Coolify (5 min)
   ↓
+12 min    Redeploy (2-3 min)
   ↓
+15 min    Testa acesso (1 min)
   ↓
✅ App está segura! 🔒
```

---

## 💡 Dicas

### Senhas Fortes
```
❌ Fraco:      123456, senha, abc123
✅ Forte:      MeuSenha$2024#Segura!
✅ Muito Forte: Ks7@mP#nQ2zX$9vR4bL!uW
```

### Compartilhar com Equipe
- Nunca mande senha por email
- Use: WhatsApp, Slack, SMS (privado)
- Cada pessoa: senha diferente
- Mude periodicamente (a cada 90 dias)

### Segurança Extra
- HTTPS: Já ativado no Coolify ✓
- Firewall: Configure se possível
- Logs: Monitore acessos

---

## 🎉 Pronto!

Sua aplicação agora está **100% protegida! 🔒**

Qualquer dúvida, volte aos documentos de segurança.

**Quer implementar agora?**

1. Gere o `.htpasswd`
2. Commite para GitHub
3. Configure no Coolify
4. **Sua app está segura!**

