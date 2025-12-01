# Situação dos Usuários e Próximos Passos

## 📊 Estado Atual (2025-12-01)

### Usuários no Sistema

**Antes da última redeploy:**
- `marco` (admin principal)
- `kennedy.oliveira` (criado na aplicação)
- `alisson.galvao` (criado na aplicação)
- `marcos.fernandes` (criado na aplicação)

**Depois da última redeploy:**
- `marco` ✅ (apenas este permanece em credentials.json)
- `kennedy.oliveira` ❌ (desapareceu)
- `alisson.galvao` ❌ (desapareceu)
- `marcos.fernandes` ❌ (desapareceu)

### Problema Raiz

Quando o Coolify fez redeploy:
1. ✅ Clonou o repositório git
2. ✅ Executou o Dockerfile
3. ✅ Copiou `credentials.json` do git (que contém apenas "marco")
4. ❌ Sobrescreveu o arquivo local com a versão do git
5. ❌ Os 3 usuários criados dinamicamente foram perdidos

### Causa: Falta de Sincronização com Banco de Dados

- Usuários criados na interface Streamlit → gravados apenas em `credentials.json` local
- `credentials.json` sincroniza com `config.yaml` ✅
- Mas nenhum sincroniza com o PostgreSQL ❌
- Quando container reinicia: arquivo local é sobrescrito pela versão do git

## 🔍 Verificação Necessária

**Execute no terminal Coolify:**

```bash
cd /app && python verificar_usuarios_postgres.py
```

Isso irá mostrar:

```
═══════════════════════════════════════════════════════════════════
📊 VERIFICAÇÃO: Usuários no PostgreSQL
═══════════════════════════════════════════════════════════════════
Total de usuários no banco: ?

Username             Email                          Status       Criado em
──────────────────────────────────────────────────────────────────────────
...
```

**Possíveis resultados:**

- **Se 4 usuários aparecerem:** Os dados estão no banco! Podemos recuperar.
- **Se apenas "marco" aparecer:** Os 3 usuários foram perdidos antes da migração.

## 📋 Plano de Solução em 3 Fases

### Fase 1: Diagnóstico (AGORA)

Execute:
```bash
python verificar_usuarios_postgres.py
```

Você verá quantos usuários realmente foram salvos no PostgreSQL.

### Fase 2: Recuperação (Dependendo do resultado)

**Opção A - Se 4 usuários estão no PostgreSQL:**
```bash
# Exportar todos os usuários do banco
python migrate_users_to_postgres.py --export-to-credentials
```

**Opção B - Se apenas "marco" está no PostgreSQL:**
- Os 3 usuários foram perdidos
- Precisará criá-los novamente (desculpe!)

### Fase 3: Prevenção Permanente

Implementar **sincronização bidirecional com PostgreSQL**:

1. ✅ Quando usuário é criado na interface → grava no PostgreSQL
2. ✅ Quando usuário faz login → carrega do PostgreSQL
3. ✅ Quando container reinicia → carrega do PostgreSQL (não do git)
4. ✅ Credenciais no git são apenas backup, não fonte de verdade

## 🗂️ Arquivos Envolvidos

| Arquivo | Status | Ação |
|---------|--------|------|
| `credentials.json` | ⚠️ Apenas "marco" | Aguardando recuperação |
| `config.yaml` | ⚠️ Apenas "marco" | Aguardando recuperação |
| `PostgreSQL usuarios` | ❓ Verificar | Execute script de verificação |
| `migrate_users_to_postgres.py` | ✅ Criado | Migração de credentials.json → BD |
| `verificar_usuarios_postgres.py` | ✅ Novo | Verificação do estado atual |
| `src/app_streamlit.py` | ⏳ Precisará atualizar | Integração com PostgreSQL |

## 🎯 Próximas Ações

### Imediato (Próximas 24h)

1. **Execute verificação:**
   ```bash
   python verificar_usuarios_postgres.py
   ```

2. **Compartilhe resultado** - Mostre quantos usuários estão no PostgreSQL

### Curto Prazo (Próximos dias)

Baseado no resultado, faremos:

- **Se 4 usuários:** Recuperar dados do banco e atualizar credentials.json
- **Se 1 usuário:** Aceitar a perda e implementar proteção imediata

### Médio Prazo (Próxima semana)

- Atualizar `src/app_streamlit.py` para autenticar via PostgreSQL
- Remover dependência de `credentials.json` como fonte de dados
- Fazer login/logout/criação de usuários diretamente com banco

## 📝 Resumo da Situação

| Aspecto | Status | Impacto |
|--------|--------|---------|
| Marco (admin) | ✅ Íntegro | Pode acessar |
| Kennedy/Alisson/Marcos | ❌ Desaparecidos | Não conseguem acessar |
| Sincronização JSON | ✅ Funcionando | credentials.json ↔ config.yaml |
| Sincronização PostgreSQL | ❌ Não existe | Usuários não sincronizam com BD |
| Git como backup | ✅ Funciona | Impede perda total mas apenas tem marco |
| Redeploy seguro | ❌ Ainda não | Arquivo local é sobrescrito |

## 🔐 O que não fazer mais

❌ Ignorar credenciais do git (causa "file not found")
❌ Criar credenciais automaticamente no load (causa reset)
❌ Manter só no archivo local (perde na redeploy)
✅ Manter no PostgreSQL como fonte de verdade
✅ Usar git como backup apenas
✅ Sincronizar app ↔ database a cada operação

---

**Próximo passo:** Execute `python verificar_usuarios_postgres.py` no terminal Coolify e compartilhe o resultado!
