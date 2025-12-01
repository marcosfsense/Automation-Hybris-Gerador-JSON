# Gestão de Usuários e PostgreSQL

## Status Atual

### Situação dos Usuários (2025-12-01)

**PostgreSQL:**
- Conectado e funcional: `u48cw44ccwg4sowco4044goc:5432`
- Tabela `usuarios` criada e pronta
- Usuários no banco: **1 apenas** (marco)
  - marco: marco@example.com ✅

**Usuários Perdidos:**
- kennedy.oliveira ❌
- alisson.galvao ❌
- marcos.fernandes ❌

### Causa Raiz

Os 3 usuários foram criados na interface Streamlit e salvos apenas em `credentials.json` local. Quando o container redeployou, a versão do git (que contém apenas "marco") sobrescreveu o arquivo local, causando a perda permanente dos dados.

**Raiz do problema:** Falta de sincronização automática entre aplicação e PostgreSQL.

---

## Solução Implementada

### Fase 1: Diagnóstico ✅ (Concluída)

- Verificação PostgreSQL executada
- Confirmado: apenas "marco" no banco
- Documentação do problema e plano de solução

### Fase 2: Recuperação (Em andamento)

**O que você precisa fazer:**

1. **Recriar os 3 usuários** na aplicação:
   - kennedy.oliveira
   - alisson.galvao
   - marcos.fernandes

2. **Verificar sincronização** com PostgreSQL:
   ```bash
   cd /app && python verificar_usuarios_postgres.py
   ```

### Fase 3: Implementação Permanente (Próxima semana)

Implementar sincronização automática:

```python
# ANTES (❌):
Criar usuário → Salva em credentials.json (pode ser sobrescrito)

# DEPOIS (✅):
Criar usuário → Salva em credentials.json AND PostgreSQL
Redeploy → Carrega do PostgreSQL (fonte de verdade)
```

---

## Scripts Disponíveis

### verificar_usuarios_postgres.py
Mostra todos os usuários no banco:
```bash
cd /app && python verificar_usuarios_postgres.py
```

### migrate_users_to_postgres.py
Migra usuários de credentials.json para PostgreSQL (já executado):
```bash
cd /app && python migrate_users_to_postgres.py
```

---

## Timeline

| Semana | Atividade | Status |
|--------|-----------|--------|
| Esta semana | Recriar 3 usuários | ⏳ Aguardando |
| Próxima semana | Implementar sincronização | ⏳ Planejado |
| Após implementação | Nenhum usuário será mais perdido | ✨ Objetivo |

---

## Próximas Ações

1. **Recriar os 3 usuários** na aplicação
2. **Executar verificação**: `python verificar_usuarios_postgres.py`
3. **Aguardar implementação** de sincronização (próxima semana)

Para detalhes técnicos, consulte `GUIA_GERENCIAR_USUARIOS.md`.
