# 🎨 Como Ativar Tema Escuro e Settings no Coolify

## ✅ O que foi alterado

Atualizei o arquivo `.streamlit/config.toml` com as seguintes mudanças:

### Antes ❌
```toml
[client]
toolbarMode = "minimal"  # Esconde o botão Settings

[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"  # Branco
```

### Depois ✅
```toml
[client]
toolbarMode = "auto"  # Mostra o botão Settings

[theme]
base = "dark"  # Tema escuro como padrão
backgroundColor = "#0e1117"  # Cinza escuro
```

---

## 🚀 Como Aplicar no Coolify

### Opção 1: Redeploy Automático (Recomendado)
Se você ativou "Auto Deploy on Push" no Coolify:

1. ✅ **Já feito!** Push foi feito automaticamente para GitHub
2. Coolify vai detectar a mudança em ~1 minuto
3. Iniciará rebuild automático
4. Aguarde ~3-5 minutos
5. Recarregue a página do navegador (F5)
6. Tema escuro + Settings estarão disponíveis

**Tempo até estar online:** ~5 minutos

---

### Opção 2: Redeploy Manual (Se Auto Deploy não está ativado)

1. No Coolify, vá para seu aplicativo (Gerador JSON Hybris)
2. Clique em "Deployments"
3. Clique em "Trigger Deployment" ou "Redeploy"
4. Aguarde a build terminar (~3-5 minutos)
5. Recarregue a página (F5)

**Tempo até estar online:** ~5 minutos

---

## 🎯 O que Esperar Após a Atualização

### ✨ Novo Comportamento

1. **Botão Settings aparece** (canto superior direito)
   - Ícone: ⚙️ ou "Settings"

2. **Tema Escuro como Padrão**
   - Cores: Preto/Cinza escuro
   - Texto: Branco/Cinza claro

3. **Usuário pode Mudar Tema**
   - Clique em ⚙️ Settings
   - Procure por "Theme"
   - Escolha "Light" ou "Dark"
   - Preferência é salva no navegador

---

## 🎨 Cores Atualizadas

| Elemento | Cor Anterior | Cor Nova |
|----------|-------------|----------|
| Fundo | #FFFFFF (Branco) | #0e1117 (Cinza Escuro) |
| Fundo Secundário | #F0F2F6 (Cinza Claro) | #161b22 (Cinza Médio) |
| Texto | #262730 (Cinza Escuro) | #c9d1d9 (Cinza Claro) |
| Botão Primário | #FF6B6B (Vermelho) | #FF6B6B (Vermelho - mantido) |

---

## 📋 Checklist Pós-Atualização

- [ ] Coolify iniciou rebuild (procure em "Deployments")
- [ ] Aguardou 3-5 minutos para build terminar
- [ ] Recarregou página (Ctrl+F5 ou Cmd+Shift+R)
- [ ] Botão Settings (⚙️) aparece no canto superior direito
- [ ] Página abre com tema escuro
- [ ] Clicou em Settings e viu opção de mudar tema
- [ ] Mudou para "Light" e depois voltou para "Dark"
- [ ] Recarregou página e tema "Dark" manteve-se (salvo no navegador)

**Quando todos estiverem marcados: ✅ Tudo funcionando!**

---

## 🔧 Personalizar Cores (Opcional)

Se quiser mudar as cores do tema escuro, edite `.streamlit/config.toml`:

```toml
[theme]
base = "dark"
primaryColor = "#FF6B6B"           # Cor dos botões
backgroundColor = "#0e1117"        # Fundo principal
secondaryBackgroundColor = "#161b22" # Fundo das caixas
textColor = "#c9d1d9"              # Cor do texto
```

**Depois de editar:**
1. Faça push para GitHub (`git add` → `git commit` → `git push`)
2. Coolify detecta mudança e redeploy automático
3. Aguarde 3-5 minutos
4. Recarregue página

---

## 🆘 Se Não Funcionar

### Problema 1: "Settings ainda não aparece"
**Solução:**
1. Aguarde mais 5 minutos (build pode estar em andamento)
2. Clique "Refresh" ou recarregue página (Ctrl+F5)
3. Limpe cache do navegador (Ctrl+Shift+Delete)
4. Tente outra aba/navegador

### Problema 2: "Tema escuro, mas não salva a preferência"
**Solução:**
1. Verifique se aceita cookies no navegador
2. Limpe cache do navegador
3. Tente novamente

### Problema 3: "Cores estranhas ou fora de padrão"
**Solução:**
1. Clique em Settings → Theme → escolha padrão "Light" ou "Dark"
2. Recarregue página

---

## 📞 Resumo Rápido

| Ação | Status |
|------|--------|
| Código atualizado | ✅ Feito |
| Push para GitHub | ✅ Feito |
| Aguardando redeploy? | ⏳ 3-5 minutos |
| Settings visível? | ✅ Sim (após redeploy) |
| Tema escuro padrão? | ✅ Sim (após redeploy) |
| Posso mudar o tema? | ✅ Sim (via Settings) |

---

## 💡 Dica Final

Se quiser reverter para tema claro como padrão, apenas altere:

```toml
[theme]
base = "light"  # ao invés de "dark"
```

E faça push novamente. A mudança será aplicada automaticamente no Coolify!

**Tudo pronto! Tema escuro está a caminho! 🚀**

