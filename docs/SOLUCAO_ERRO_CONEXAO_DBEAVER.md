# Solução - Erro de Conexão PostgreSQL no DBeaver

**Status**: Troubleshooting do erro "A tentativa de conexão falhou"
**Erro**: `u48cw44ccwg4sowco4044goc - A tentativa de conexão falhou`
**Data**: 2025-12-02

---

## 🔴 Problema Identificado

O host `u48cw44ccwg4sowco4044goc` **não está resolvendo** de fora da VPS.

Possíveis razões:
1. Host é um **nome interno** (apenas dentro da VPS)
2. Host está **offline** ou não acessível
3. **Firewall** bloqueando porta 5432
4. **DNS** não resolvendo o hostname

---

## ✅ Soluções

### Opção 1: Verificar se PostgreSQL está rodando (NA VPS)

Se você tiver acesso SSH à VPS:

```bash
# Conectar à VPS via SSH
ssh seu_usuario@seu_vps_ip

# Verificar se PostgreSQL está rodando
sudo systemctl status postgresql

# Se não estiver rodando:
sudo systemctl start postgresql
```

---

### Opção 2: Usar IP ao invés de Hostname

O hostname `u48cw44ccwg4sowco4044goc` pode ser interno. **Você precisa do IP real da VPS.**

**Qual é o IP da sua VPS?**

Se souber o IP, use no DBeaver:

**Na tela de conexão do DBeaver:**

```
Host:     seu_vps_ip_aqui    (ex: 192.168.1.100 ou 50.123.45.67)
Port:     5432
Database: postgres
User:     postgres
Password: poMaf572450+@
```

---

### Opção 3: Verificar Firewall da VPS

Se o IP funciona mas ainda dá erro, verifique firewall:

```bash
# Na VPS, verificar se porta 5432 está aberta
sudo ufw status

# Se não estiver aberta, permitir:
sudo ufw allow 5432/tcp

# Ou no iptables:
sudo iptables -A INPUT -p tcp --dport 5432 -j ACCEPT
```

---

### Opção 4: Verificar PostgreSQL Listen Address

PostgreSQL pode estar configurado para aceitar apenas conexões locais:

```bash
# Na VPS, abrir arquivo de config
sudo nano /etc/postgresql/*/main/postgresql.conf

# Procurar por:
# listen_addresses = 'localhost'

# E mudar para:
listen_addresses = '*'

# Salvar (Ctrl+X, Y, Enter)

# Depois, editar pg_hba.conf:
sudo nano /etc/postgresql/*/main/pg_hba.conf

# Adicionar ao final:
host    all             all             0.0.0.0/0               md5

# Reiniciar PostgreSQL:
sudo systemctl restart postgresql
```

---

## 🎯 Passo-a-Passo para Solucionar

### 1️⃣ Descobrir o IP Real da VPS

Se está usando Coolify/Docker, procure por:

```
Coolify Dashboard → Seu Projeto → Settings
→ Procure por "IP" ou "Host"
```

**Ou**, use comando no terminal local:

```bash
# Tentar ping
ping u48cw44ccwg4sowco4044goc

# Se der erro "Unknown host", é um hostname interno
# Procure no painel da VPS pelo IP real
```

---

### 2️⃣ Testar Conectividade

```bash
# Testar se consegue acessar porta 5432
telnet seu_vps_ip 5432

# Se conseguir:
Connected to ...

# Se der erro:
telnet: Unable to connect to remote host: Connection refused
```

---

### 3️⃣ No DBeaver, Use o IP

```
Host:     seu_vps_ip_real
Port:     5432
Database: postgres
User:     postgres
Password: poMaf572450+@
```

Clique **Test Connection**

---

## 🆘 Cenários Comuns

### Cenário A: Usando Coolify (Docker)

Se está usando Coolify, o PostgreSQL provavelmente está **dentro do Docker**, não acessível de fora.

**Soluções:**

1. **Via SSH no Coolify Server**:
   ```bash
   # SSH para o servidor Coolify
   ssh seu_usuario@coolify_server_ip

   # Dentro, conectar ao container PostgreSQL
   docker exec -it seu_container_postgres psql -U postgres -d postgres
   ```

2. **Expor PostgreSQL**:
   - Coolify → Seu Projeto → Container → Port Mapping
   - Adicionar mapeamento: `5432:5432`
   - Reiniciar container
   - Usar `localhost:5432` ou `coolify_ip:5432`

---

### Cenário B: PostgreSQL em VPS Separada

Se PostgreSQL está em uma VPS diferente:

```
VPS-App (Coolify/Streamlit)  →  VPS-DB (PostgreSQL)
```

**Você precisa do IP da VPS-DB!**

Peça ao seu fornecedor:
- IP ou Hostname da VPS que tem PostgreSQL
- Porta (padrão é 5432)
- Se firewall precisa de liberação

---

### Cenário C: PostgreSQL Local (Dev)

Se está desenvolvendo localmente:

```
Host:     localhost
Port:     5432
Database: postgres
User:     postgres
Password: poMaf572450+@
```

---

## 📋 Checklist de Verificação

Antes de reportar erro:

- [ ] Tenho o IP correto da VPS?
- [ ] PostgreSQL está rodando na VPS?
- [ ] Porta 5432 está aberta no firewall?
- [ ] Consigo fazer ping para o IP?
- [ ] Consigo fazer telnet para porta 5432?
- [ ] Usei o IP (não o hostname) no DBeaver?
- [ ] Senha exatamente: `poMaf572450+@` (com @ e +)?
- [ ] User é: `postgres`?

---

## 🔧 Encontrar IP da VPS

### Se está em Coolify:

```
Coolify Web Interface:
  Settings → Server → IP Address
```

### Se tem acesso SSH:

```bash
ssh seu_usuario@seu_vps_host
hostname -I
# Mostra: 192.168.1.100 (ou seu IP)
```

### Se está em Docker local:

```bash
# Listar containers
docker ps

# Ver IP do container PostgreSQL
docker inspect nome_container | grep IPAddress

# Usar esse IP
```

---

## 💡 Dica Final

**Se tudo falhar**, conecte via SSH + psql:

```bash
# SSH para VPS
ssh seu_usuario@seu_vps_ip

# Depois, conectar via psql
psql -h localhost -U postgres -d postgres

# Digitar senha quando pedir
```

Isso prova que PostgreSQL está rodando e a senha está correta!

---

## 📞 Informações que Preciso

Se ainda não funcionar, me envie:

1. ✅ Qual é o **IP ou hostname** da VPS com PostgreSQL?
2. ✅ Qual é o **fornecedor** (Linode, DigitalOcean, AWS, Coolify, outro)?
3. ✅ Está em **Docker** ou **instalado diretamente**?
4. ✅ Output de: `telnet seu_vps_ip 5432`
5. ✅ Output do teste de conexão no DBeaver (botão **<< Detalhes**)

Com essas informações, consigo resolver definitivamente!

---

**Próxima ação**: Descobra o IP real da sua VPS e tente novamente! 🚀
