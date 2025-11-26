# 👥 Gerenciar Usuários - Interface Gráfica (Streamlit)

## 🎯 Visão Geral

Você pode gerenciar usuários de **duas formas**:

1. **Interface Gráfica (Streamlit)** - Recomendado para iniciantes
2. **Terminal (Script Python)** - Mais rápido para usuários avançados

Este guia foca na **interface gráfica integrada** no Streamlit!

---

## 📱 Como Começar

### PASSO 1: Fazer Login
1. Acesse: `https://gerajson.sensebike.com.br` (produção) ou `streamlit run src/app_streamlit.py` (local)
2. Digite o usuário e senha:
   - **Usuário:** marco
   - **Senha:** SenhaForte123!Marcos

### PASSO 2: Ir para Gerenciar Usuários
1. Na barra lateral esquerda, você verá:
   ```
   📋 Escolha uma opção:
   ⭕ 🚀 Gerador JSON
   ⭕ 👥 Gerenciar Usuários
   ```
2. Clique em: **👥 Gerenciar Usuários**

### PASSO 3: Escolher a Ação
Você verá no sidebar esquerdo 4 opções:
```
⚙️ Opções:
  📋 Listar Usuários
  ➕ Criar Usuário
  🔑 Alterar Senha
  ❌ Remover Usuário
```

---

## 📋 OPÇÃO 1: Listar Usuários

### Como Usar
1. Clique em: **📋 Listar Usuários**
2. Você verá todos os usuários cadastrados em uma tabela

### Exemplo de Resultado
```
👤 marco
   Status: ✅ Ativo
   Criado: 2025-11-26 10:30:45
   Último: 2025-11-26 11:15:22

👤 joao
   Status: ✅ Ativo
   Criado: 2025-11-26 10:35:10
   Último: Nunca
```

---

## ➕ OPÇÃO 2: Criar Novo Usuário

### Como Usar
1. Clique em: **➕ Criar Usuário**
2. Preencha o formulário:
   - **Nome do usuário:** (ex: joao, maria, carlos)
   - **Senha:** (mínimo 8 caracteres)
   - **Confirmar senha:** (repita a senha)
3. Clique em: **✅ Criar Usuário**

### Exemplo
```
Nome do usuário: joao
Senha:          Senha@Joao2024
Confirmar:      Senha@Joao2024

[Clique em ✅ Criar Usuário]

Resultado: ✅ Usuário 'joao' criado com sucesso! 🎉
```

### Requisitos
- ✅ Nome: mínimo 3 caracteres
- ✅ Senha: mínimo 8 caracteres
- ✅ Pode usar símbolos: !@#$%^&*

---

## 🔑 OPÇÃO 3: Alterar Senha

### Como Usar
1. Clique em: **🔑 Alterar Senha**
2. Escolha o usuário no dropdown
3. Digite a nova senha:
   - **Nova senha:** (mínimo 8 caracteres)
   - **Confirmar:** (repita a senha)
4. Clique em: **✅ Alterar Senha**

### Exemplo
```
Selecione o usuário: [marco ▼]
Nova senha:          SenhaNovaForte2024!
Confirmar:           SenhaNovaForte2024!

[Clique em ✅ Alterar Senha]

Resultado: ✅ Senha de 'marco' alterada com sucesso! 🎉
```

---

## ❌ OPÇÃO 4: Remover Usuário

### Como Usar
1. Clique em: **❌ Remover Usuário**
2. Escolha o usuário para remover
3. Você verá um aviso:
   ```
   ⚠️ Você está prestes a remover o usuário 'joao'.
   Esta ação não pode ser desfeita!
   ```
4. Clique em: **❌ Confirmar Remoção**

### Exemplo
```
Selecione o usuário: [joao ▼]

⚠️ Você está prestes a remover o usuário 'joao'.
Esta ação não pode ser desfeita!

[❌ Confirmar Remoção]  [🔙 Cancelar]

Resultado: ✅ Usuário 'joao' removido com sucesso! ✅
```

---

## 🎯 Fluxo Visual Completo

```
┌─────────────────────────────────────┐
│        🔐 Login na Aplicação        │
│  Usuário: marco                     │
│  Senha: SenhaForte123!Marcos        │
└────────────────┬────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│      Menu Principal (Sidebar)       │
│  ⭕ 🚀 Gerador JSON                │
│  ⭕ 👥 Gerenciar Usuários          │
└────────────────┬────────────────────┘
                 ↓
        (clica em 👥)
                 ↓
┌─────────────────────────────────────┐
│    Página: Gerenciar Usuários       │
│  ⚙️ Opções:                         │
│  ○ 📋 Listar Usuários              │
│  ○ ➕ Criar Usuário                │
│  ○ 🔑 Alterar Senha                │
│  ○ ❌ Remover Usuário              │
└────────────────┬────────────────────┘
          ┌──────┴──────┬────────┬──────┐
          ↓             ↓        ↓      ↓
      Listar        Criar    Alterar Remover
      Usuários     Usuário    Senha   Usuário
          ↓             ↓        ↓      ↓
       Tabela      Formulário Dropdown Aviso
                        ↓        ↓      ↓
                     Salva    Salva  Confirmação
                        ↓        ↓      ↓
                    ✅ Criado ✅ Alterado ✅ Removido
```

---

## 🔄 Sincronizando com Coolify (Deploy)

### ⚠️ IMPORTANTE
As mudanças são salvas automaticamente no arquivo `credentials.json`, mas para que funcionem em **produção**, você precisa:

### PASSO 1: Fazer Commit no GitHub
1. Abra **Git Bash** ou **Prompt de Comando**
2. Navegue até a pasta:
   ```bash
   cd "c:\Users\marcos.fernandes\Desktop\AUTOMAÇÃO HYBRIS - GERADOR DE JSONs"
   ```
3. Execute os comandos:
   ```bash
   git status              # Ver o que mudou
   git add credentials.json
   git commit -m "chore: Gerenciar usuarios"
   git push origin main
   ```

### PASSO 2: Fazer Redeploy no Coolify
1. Abra seu **Coolify**: https://coolify.sensebike.com.br
2. Navegue até: **Gerador-JSON-Hybris** → **Deployments**
3. Clique em: **"Redeploy"** (botão vermelho)
4. Aguarde: ~1-2 minutos (rápido, sem rebuild do Docker)
5. Status muda para: **"Successful"** (verde)

### PASSO 3: Testar Novo Usuário
1. Abra: https://gerajson.sensebike.com.br
2. Teste login com novo usuário:
   ```
   Usuário: joao
   Senha:   Senha@Joao2024
   ```
3. Deve funcionar! ✅

---

## 💡 Dicas e Boas Práticas

### ✅ BOAS PRÁTICAS
1. **Sempre faça Redeploy após mudanças**
   - Sem redeploy, mudanças não funcionam em produção

2. **Use senhas fortes**
   - 12+ caracteres, misture maiúsculas, números, símbolos

3. **Teste localmente antes de deploy**
   - Execute `streamlit run src/app_streamlit.py` para testar

4. **Mantenha log de usuários**
   - Guarde informação de quem tem acesso

5. **Altere a senha padrão do marco**
   - Nunca deixe a senha padrão em produção

### ❌ ERROS COMUNS
1. ❌ Criar usuário com senha muito curta
   - Use mínimo 8 caracteres (recomendo 12+)

2. ❌ Esquecer de fazer Redeploy
   - Mudança local não funciona em produção

3. ❌ Remover o único usuário
   - Sempre mantenha pelo menos um usuário ativo

4. ❌ Usar mesmo usuário para múltiplas pessoas
   - Crie usuário diferente para cada pessoa

---

## 🆘 Problemas e Soluções

### Problema: "Não consigo entrar na página de Gerenciar Usuários"
**Solução:**
1. Certifique-se de que fez login corretamente
2. A opção "👥 Gerenciar Usuários" aparece no sidebar?
3. Se não aparecer, recarregue a página: Ctrl+F5

### Problema: "Fiz redeploy mas usuário novo não funciona"
**Solução:**
1. Aguarde 2-3 minutos após redeploy
2. Recarregue a página no navegador: Ctrl+F5
3. Limpe cache: Ctrl+Shift+Delete
4. Tente fazer login novamente

### Problema: "Esqueci qual é a senha do marco"
**Solução:**
1. Abra Prompt de Comando
2. Execute:
   ```bash
   cd "c:\Users\marcos.fernandes\Desktop\AUTOMAÇÃO HYBRIS - GERADOR DE JSONs"
   python manage_users.py reset-all
   ```
3. Responda: `s` (sim)
4. Senha volta a ser: **SenhaForte123!Marcos**
5. Não esqueça de fazer commit e redeploy!

---

## 📊 Comparação: Streamlit vs Terminal

| Ação | Terminal (Script) | Streamlit (Interface) |
|------|-------------------|-----------------------|
| **Listar usuários** | `python manage_users.py list` | Clique e vê tabela visual |
| **Criar usuário** | `python manage_users.py add joao Senha@123` | Preencha formulário com validação |
| **Alterar senha** | `python manage_users.py change marco Nova!` | Dropdown e formulário |
| **Remover usuário** | `python manage_users.py remove joao` | Dropdown com confirmação |
| **Dificuldade** | ⭐⭐⭐ (complexo) | ⭐ (simples) |
| **Tempo de aprendizado** | 30 minutos | 2 minutos |

---

## 🎯 Resumo Rápido

**Para Criar Novo Usuário:**
1. Login → Sidebar "👥 Gerenciar" → "➕ Criar" → Preencher → Enviar
2. Commit e Push do `credentials.json`
3. Redeploy no Coolify

**Para Alterar Senha:**
1. Login → Sidebar "👥 Gerenciar" → "🔑 Alterar" → Escolher e Preencher
2. Commit e Push do `credentials.json`
3. Redeploy no Coolify

**Para Remover Usuário:**
1. Login → Sidebar "👥 Gerenciar" → "❌ Remover" → Escolher → Confirmar
2. Commit e Push do `credentials.json`
3. Redeploy no Coolify

---

## 🎉 Conclusão

Você agora tem uma **interface gráfica completa** para gerenciar usuários!

✅ Sem precisar de Prompt de Comando
✅ Sem precisar conhecer comandos
✅ Com validação automática
✅ Com feedback visual

**Aproveite bem!** 🚀
