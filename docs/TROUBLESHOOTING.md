# Troubleshooting - Resolução de Problemas

**Status**: Guia completo com todos os cenários conhecidos
**Última atualização**: 2025-12-01

---

## 🔍 Diagnóstico Rápido

### Passo 1: Rodar diagnóstico completo

```bash
python tools/diagnostico_completo.py
```

Este script verifica:
- ✅ Conexão PostgreSQL
- ✅ Usuários carregados
- ✅ config.yaml presente
- ✅ Sincronização

### Passo 2: Verificar logs da app

No Coolify → Logs → Procure por:

```
[startup] PASSO 1: Carregando credenciais
[startup] PASSO 2: Sincronizando para config.yaml
[startup] PASSO 3: Inicializando authenticator
[load_authenticator] OK: Authenticator inicializado com 4 usuarios
```

Se vir TODOS = ✅ Sistema OK

---

## 🔴 Problema: "User not authorized"

### Sintomas

- Apenas "marco" consegue fazer login
- Outros usuários recebem "User not authorized"
- Credenciais estão corretas (funcionam em outro lugar)

### Diagnóstico

```bash
# 1. Verificar PostgreSQL
python tools/verificar_usuarios_postgres.py

# 2. Verificar config.yaml
cat config.yaml

# 3. Comparar
python tools/diagnostico_completo.py
```

### Solução

**Cenário A: PostgreSQL tem 4, config.yaml tem 1**

```bash
# Sincronizar manualmente
python tools/debug_sync.py

# Ou reiniciar a app (vai sincronizar automaticamente)
```

**Cenário B: config.yaml vazio ou não existe**

```bash
# Forçar sincronização
python tools/debug_sync.py

# Se ainda não funcionar, verificar logs:
cat /app/logs/streamlit.log
```

**Cenário C: Ambos têm 4 usuários mas login não funciona**

```bash
# Verificar se config.yaml tem senhas corretas
python tools/debug_sync.py

# Tentar em navegador incógnito
# (às vezes cache do navegador causa problema)
```

---

## 🔴 Problema: "NameError: sync_credentials_to_config not defined"

### Sintomas

```
[startup] PASSO 2: Sincronizando para config.yaml
[startup] ERRO critico ao sincronizar: name 'sync_credentials_to_config' is not defined
```

### Causa

Função chamada ANTES de definida (estrutura do arquivo Python errada)

### Solução

✅ **Já foi corrigido no commit 982173e**

Se ainda vir este erro:
1. Verificar se rebuild foi completo (não apenas redeploy)
2. Fazer rebuild do zero:
   ```
   Coolify → Rebuild from scratch
   ```
3. Aguardar conclusão

---

## 🔴 Problema: PostgreSQL não conecta

### Sintomas

```
[load_credentials] AVISO: PostgreSQL indisponivel: connection refused
[load_credentials] Tentando fallback com credentials.json...
```

Apenas "marco" consegue fazer login (fallback ativado)

### Diagnóstico

```bash
# Verificar se PostgreSQL está rodando
ping seu-host-postgres

# Verificar credenciais
python tools/diagnostico_completo.py

# Verificar firewall
# (porta 5432 precisa estar acessível)
```

### Solução

**Se PostgreSQL indisponível**:
1. Verificar host/port em `postgres_manager.py`
2. Verificar se PostgreSQL está rodando
3. Verificar firewall/network policies
4. Verificar credenciais (user/password)

**Se não conseguir conectar**:
```bash
# Teste direto com psql
psql -h seu-host -U postgres -d postgres

# Se funciona, problema é na app
# Se não funciona, problema é no servidor PostgreSQL
```

---

## 🔴 Problema: Permissão negada em config.yaml

### Sintomas

```
[sync] ERRO ao salvar config.yaml: Permission denied
```

### Diagnóstico

```bash
# Verificar permissões
ls -la config.yaml

# Esperado:
# -rw-r--r-- 1 usuario grupo tamanho config.yaml
```

### Solução

```bash
# Dar permissão de leitura/escrita
chmod 644 config.yaml

# Ou deletar e deixar recrear
rm config.yaml
# Reiniciar app (vai recrear com permissão correta)
```

---

## 🔴 Problema: config.yaml corrompido ou inválido

### Sintomas

```
[load_authenticator] ERRO: config.yaml está vazio!
# ou
yaml.YAMLError: ...
```

### Diagnóstico

```bash
# Verificar arquivo
cat config.yaml

# Se tiver caracteres estranhos ou vazio, está corrompido
```

### Solução

```bash
# Deletar arquivo corrompido
rm config.yaml

# Reiniciar app (vai recrear corretamente)
```

---

## 🔴 Problema: Sincronização não acontece

### Sintomas

- App inicia sem erro
- Mas config.yaml não é atualizado
- PostgreSQL tem 4 usuários, config.yaml tem 1

### Diagnóstico

```bash
# Verificar logs de sync
python tools/diagnostico_completo.py

# Se mostra "[sync] OK: usuario" = sincronização funcionou
# Se não mostra = sincronização não rodou
```

### Solução

**Se logs mostram erro de sync**:
```bash
# Testar sincronização manual
python tools/debug_sync.py

# Se este script funciona, problema pode ser:
# 1. Permissão de arquivo
# 2. Espaço em disco
# 3. Problema intermitente
```

**Se logs não mostram nada de sync**:
```bash
# Função pode não estar sendo chamada
# Verificar logs procurando por:
# [startup] PASSO 2

# Se não aparecer, há problema na ordem de execução
# Fazer rebuild:
# Coolify → Rebuild from scratch
```

---

## 🟡 Problema: Login lento

### Causa Provável

PostgreSQL está longe (latência alta)

### Solução

```bash
# Verificar latência
ping seu-host-postgres

# Se > 500ms, é normal ficar lento
# Considerar cache local ou PostgreSQL mais próximo
```

---

## 🟡 Problema: "Credenciais inválidas" para todos

### Sintomas

Nenhum usuário consegue fazer login

### Diagnóstico

```bash
# 1. Verificar se authenticator inicializou
grep "Authenticator inicializado" logs

# 2. Verificar se config.yaml tem usuários
cat config.yaml

# 3. Testar credenciais manualmente
python tools/verificar_usuarios_postgres.py
```

### Solução

**Se config.yaml está vazio**:
```bash
python tools/debug_sync.py
```

**Se config.yaml tem dados mas login não funciona**:
```bash
# Pode ser problema de cache do navegador
# Usar navegador incógnito (Ctrl+Shift+P no Chrome)
```

**Se mesmo em incógnito não funciona**:
```bash
# Problema pode ser no streamlit-authenticator
# Reinstalar a biblioteca:
pip install --upgrade streamlit-authenticator
```

---

## 🟡 Problema: Session expired logo após login

### Sintomas

Login funciona mas é deslogado em segundos

### Causa Provável

Cookie expirou ou configuração incorreta

### Solução

```bash
# Verificar config.yaml
cat config.yaml | grep -A 3 cookie

# Esperado:
# cookie:
#   expiry_days: 30
#   key: gerador_json_hybris_secret_key_2025
#   name: hybris_json_generator_auth

# Se não tiver, atualizar:
python tools/debug_sync.py
```

---

## ✅ Checklist de Verificação

Antes de reportar problema:

- [ ] Rodar `python tools/diagnostico_completo.py`
- [ ] Verificar logs da app
- [ ] Testar em navegador incógnito
- [ ] Verificar conectividade PostgreSQL
- [ ] Verificar permissões de arquivo
- [ ] Verificar se config.yaml existe e é válido
- [ ] Tentar rebuild se problema persiste

---

## 📞 Como Reportar Problema

Se nada acima resolver:

1. **Rodar diagnóstico**:
   ```bash
   python tools/diagnostico_completo.py > diagnostico.txt
   ```

2. **Coletar informações**:
   - Output do diagnóstico
   - Logs da app (últimas 50 linhas)
   - Qual cenário de problema (user not authorized, NameError, etc)
   - Que tentativas já fez

3. **Reportar com**:
   - Descrição clara do problema
   - Steps para reproduzir
   - Output do diagnóstico
   - Logs relevantes

---

## 🔧 Scripts Úteis

```bash
# Diagnóstico completo
python tools/diagnostico_completo.py

# Verificar PostgreSQL
python tools/verificar_usuarios_postgres.py

# Sincronização manual
python tools/debug_sync.py

# Debug específico
python tools/debug_marcos.py

# Migração de usuários
python tools/migrate_users_to_postgres.py
```

---

## 📚 Veja Também

- [docs/AUTENTICACAO.md](AUTENTICACAO.md) - Como o sistema funciona
- [docs/GUIA_INSTALACAO.md](GUIA_INSTALACAO.md) - Setup inicial
- [docs/ESTRUTURA_PROJETO.md](ESTRUTURA_PROJETO.md) - Arquivos do projeto

---

**Última atualização**: 2025-12-01
**Status**: ✅ Todos os cenários cobertos
