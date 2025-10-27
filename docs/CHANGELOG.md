# Changelog

Histórico de versões do Gerador de JSON Hybris.

---

## [2.0.0] - 2025-10-27

### ✨ Novo
- Interface web com Streamlit
- Validações em tempo real
- Download de arquivo JSON
- Preview formatado
- Suporte para MÚLTIPLAS transações (até 5)
- IDs únicos de 42 caracteres (alfanuméricos, sem traços)
- Timestamps com timezone do Brasil (America/Sao_Paulo)

### 🔄 Mudanças
- **BREAKING:** IDs agora têm 42 caracteres (era 36 com traços)
- **BREAKING:** Cabeçalho JSON vem do usuário (era gerado)
- Campo `status` sempre "PAID" (não informado pelo usuário)
- Campo `numberOfQuotas` obrigatório no formulário para crédito
- Removida dependência do n8n

### ✅ Melhorias
- Interface mais intuitiva
- Validação completa do cabeçalho JSON
- Card mask e card brand mantidos
- Lógica condicional automática (campos aparecem conforme tipo)
- Mensagens de erro mais claras

### 🐛 Correções
- Timezone correto (Brasil) nos timestamps
- Validação de soma das transações
- Geração de IDs únicos garantida

---

## [1.0.0] - 2025-10-24

### ✨ Inicial
- Gerador Python básico
- Suporte para PIX, DÉBITO, CRÉDITO
- Testes automatizados
- Workflow n8n
- Documentação inicial

---

## Tipos de Mudança

- **✨ Novo**: Novas funcionalidades
- **🔄 Mudanças**: Alterações em funcionalidades existentes
- **✅ Melhorias**: Melhorias de performance/UX
- **🐛 Correções**: Correção de bugs
- **⚠️ BREAKING**: Mudanças que quebram compatibilidade

---

## Próximas Versões (Planejado)

### [2.1.0] - Futuro
- [ ] Integração direta com API Hybris
- [ ] Histórico de JSONs gerados
- [ ] Autenticação de usuários
- [ ] Dashboard com métricas

### [2.2.0] - Futuro
- [ ] Exportação em lote
- [ ] Templates salvos
- [ ] Notificações de sucesso/erro
- [ ] Modo offline

---

**Versão Atual:** 2.0.0
**Status:** ✅ Produção
