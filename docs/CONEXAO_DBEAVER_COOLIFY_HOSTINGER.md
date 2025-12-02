# Conexão DBeaver - Coolify no Hostinger

**Status**: Guia específico para sua configuração
**Sua VPS**: `srv1152862.hstgr.cloud` / `72.61.58.41`
**Provedor**: Hostinger (KVM2)
**App**: Coolify (Ubuntu 24.04)

---

## 🔍 Diagnóstico

Você tem tudo correto:
- ✅ IP: `72.61.58.41`
- ✅ Port: `5432`
- ✅ Database: `postgres`
- ✅ User: `postgres`
- ❌ Mas conexão não funciona

**Causa provável**: PostgreSQL está em um **container Docker** e a porta `5432` **NÃO está mapeada** para a VPS host.

---

## ✨ Solução

### Cenário A: PostgreSQL em Docker (dentro do Coolify)

Se PostgreSQL está **dentro de um container Docker** no Coolify, precisa fazer **port mapping**.

**No Coolify:**

1. Vá para seu **Projeto/Serviço PostgreSQL**
2. Clique em **"Container"** ou **"Settings"**
3. Procure por **"Port Mapping"** ou **"Ports"**
4. Deve ter algo como:
   ```
   5432:5432 (container:host)
   ```
5. Se **NÃO tiver**, adicione:
   - Container Port: `5432`
   - Host Port: `5432`
6. Clique **Save** e reinicie o container

Depois tente no DBeaver novamente.

---

### Cenário B: PostgreSQL Instalado Diretamente (não Docker)

Se PostgreSQL está instalado diretamente no Ubuntu:

#### 1️⃣ Conectar via SSH (quando backup terminar)

```bash
ssh root@72.61.58.41
# Digitar senha
```

#### 2️⃣ Verificar se PostgreSQL está rodando

```bash
sudo systemctl status postgresql
```

**Esperado:**
```
● postgresql.service - PostgreSQL RDBMS
   Loaded: loaded
   Active: active (running) ✅
```

Se estiver **stopped**, iniciar:
```bash
sudo systemctl start postgresql
```

#### 3️⃣ Verificar Listen Address

PostgreSQL pode estar configurado para aceitar **apenas conexões locais**:

```bash
sudo nano /etc/postgresql/*/main/postgresql.conf
```

Procurar por:
```
listen_addresses = 'localhost'
```

Se encontrar, mudar para:
```
listen_addresses = '*'
```

Salvar (Ctrl+X, Y, Enter)

#### 4️⃣ Editar pg_hba.conf

```bash
sudo nano /etc/postgresql/*/main/pg_hba.conf
```

Adicionar ao final:
```
host    all             all             0.0.0.0/0               md5
host    all             all             ::/0                    md5
```

Salvar.

#### 5️⃣ Reiniciar PostgreSQL

```bash
sudo systemctl restart postgresql
```

#### 6️⃣ Verificar porta aberta

```bash
sudo lsof -i :5432
```

**Esperado:**
```
postgres  1234  postgres    3u  IPv6  12345      0t0  TCP *:5432 (LISTEN)
```

Se não aparecer, PostgreSQL não está escutando na porta!

---

## 🔒 Firewall - IMPORTANTE!

A porta `5432` pode estar bloqueada pelo firewall do Hostinger ou Ubuntu.

### Opção 1: UFW (Ubuntu Firewall)

```bash
# Ver status
sudo ufw status

# Se estiver ativo, permitir porta 5432
sudo ufw allow 5432/tcp

# Verificar
sudo ufw status
```

### Opção 2: Firewall Hostinger

No painel Hostinger:
1. **Configurações → Segurança → Firewall**
2. Procurar por **"Porta 5432"**
3. Se não estiver liberada, liberar para seu IP local

### Opção 3: Verificar com Telnet

Do seu computador local:

```bash
telnet 72.61.58.41 5432
```

**Se conectar:**
```
Connected to 72.61.58.41
Escape character is '^]'.
```
→ Porta aberta ✅

**Se não conectar:**
```
telnet: Unable to connect to remote host: Connection refused
```
→ Firewall bloqueando ❌

---

## 🎯 Passo-a-Passo Completo

### Quando Conseguir Acessar SSH:

```bash
# 1. Conectar
ssh root@72.61.58.41

# 2. Verificar PostgreSQL
sudo systemctl status postgresql

# 3. Se stopped, iniciar
sudo systemctl start postgresql

# 4. Testar localmente
psql -U postgres -d postgres -c "SELECT version();"

# 5. Verificar porta
sudo lsof -i :5432

# 6. Se não aparecer, editar postgresql.conf
sudo nano /etc/postgresql/*/main/postgresql.conf
# Mudar: listen_addresses = '*'
# Salvar

# 7. Editar pg_hba.conf
sudo nano /etc/postgresql/*/main/pg_hba.conf
# Adicionar:
# host    all             all             0.0.0.0/0               md5
# Salvar

# 8. Reiniciar
sudo systemctl restart postgresql

# 9. Verificar firewall
sudo ufw status
sudo ufw allow 5432/tcp

# 10. Sair
exit
```

### Depois no DBeaver:

```
Host:     72.61.58.41
Port:     5432
Database: postgres
User:     postgres
Password: poMaf572450+@
```

Clique **"Test Connection"** → Deve funcionar! ✅

---

## 🆘 Se Ainda Não Funcionar

### Teste 1: Telnet Local

```bash
telnet 72.61.58.41 5432
```

**Resultado esperado**: Connected (porta aberta)
**Se recusar**: Firewall ou PostgreSQL não está escutando

### Teste 2: Conectar via SSH + psql

```bash
ssh root@72.61.58.41
psql -U postgres -c "\l"
# Lista os bancos de dados
```

Se isso funcionar = PostgreSQL está rodando ✅
Se não funcionar = Problema no PostgreSQL

### Teste 3: Verificar Listen Address

```bash
ssh root@72.61.58.41
sudo -u postgres psql -c "SHOW listen_addresses;"
```

**Esperado**: `*` (asterisco)
**Se for `localhost`**: Editar postgresql.conf

---

## 📋 Checklist

Antes de reportar problema:

- [ ] Aguardei o backup terminar?
- [ ] Consegui conectar SSH?
- [ ] PostgreSQL está rodando? (`systemctl status postgresql`)
- [ ] `listen_addresses = '*'` em postgresql.conf?
- [ ] Firewall permite porta 5432? (`ufw allow 5432/tcp`)
- [ ] Testei com telnet?
- [ ] Testei `psql` via SSH?

---

## 💡 Resumo Rápido

**Se PostgreSQL em Docker (Coolify):**
→ Adicionar port mapping `5432:5432` no Coolify

**Se PostgreSQL instalado (Ubuntu):**
→ Editar postgresql.conf + pg_hba.conf + ufw + reiniciar

**Depois:**
→ No DBeaver use IP `72.61.58.41`

---

## 📞 Informações para Debug

Quando conseguir acessar SSH, me envie output de:

```bash
sudo systemctl status postgresql
sudo lsof -i :5432
sudo -u postgres psql -c "SHOW listen_addresses;"
sudo ufw status
```

Com essas informações consigo resolver!

---

**Próximo passo**: Aguardar backup terminar → Acessar SSH → Seguir o guia acima! 🚀
