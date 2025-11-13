# 🐍 Guia Completo de Instalação do Python

> Este guia cobre todas as formas de instalar Python para usar o Gerador JSON Hybris

---

## ⚡ Forma Mais Fácil (Recomendada)

### Opção 1A: Instalador Automático Windows (1 clique!)

Se está no Windows, **a forma mais fácil é usar o script instalador automático**:

```
👉 Duplo clique em: instalar_python.bat
```

**O que ele faz:**
1. ✅ Verifica se Python já está instalado
2. ✅ Se não estiver, oferece download automático
3. ✅ Instala Python 3.11 automaticamente
4. ✅ Instala as dependências (Streamlit)
5. ✅ Inicia a aplicação

**Pronto em 2-3 minutos!** ⏱️

---

## 📋 Opção 1B: Manual Passo-a-Passo (Windows/Mac/Linux)

Se o instalador automático não funcionar, siga este guia:

### Passo 1️⃣: Baixar Python

1. Acesse: **https://www.python.org/downloads/**

2. Clique no botão **amarelo grande** com a versão mais recente

   ![Python Download](https://via.placeholder.com/400x200?text=Python+Download+Button)

3. Escolha **Windows Installer (64-bit)**
   - Arquivo: `python-3.11.X-amd64.exe`

### Passo 2️⃣: Instalar Python

1. **Execute o instalador** (duplo clique no arquivo `.exe` baixado)

2. **⚠️ IMPORTANTE:** Marque a opção **"Add Python to PATH"**

   ![Add to PATH](https://via.placeholder.com/400x200?text=Add+Python+to+PATH)

   **Isso é ESSENCIAL!** Sem isso, o sistema não encontrará Python.

3. Clique em **"Install Now"**

4. Aguarde a instalação (2-3 minutos)

5. Clique em **"Close"** quando terminar

### Passo 3️⃣: Verificar Instalação

Abra **CMD** ou **PowerShell** e execute:

```bash
python --version
```

Você deve ver algo como:
```
Python 3.11.7
```

Se vir algo diferente ou "comando não encontrado", **reinicie o computador** e tente novamente.

---

## 🛠️ Opção 2: Instalar via Gerenciador (Mac/Linux)

### Mac (usando Homebrew)

Se tem Homebrew instalado:

```bash
brew install python@3.11
```

### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3.11 python3-pip
```

### Linux (Fedora/CentOS)

```bash
sudo dnf install python3.11 python3-pip
```

---

## 🐳 Opção 3: Docker (Avançado)

Se está familiarizado com Docker, pode usar uma imagem Python pronta:

```bash
docker run -it -p 8501:8501 -v $(pwd):/app python:3.11 /bin/bash
cd /app
pip install -r requirements.txt
streamlit run src/app_streamlit.py
```

---

## ✅ Depois de Instalar Python

### Passo 1: Clone o Repositório

```bash
# Com Git
git clone https://github.com/marcosfsense/AUTOMA--O-HYBRIS---GERADOR-DE-JSONs.git
cd AUTOMA--O-HYBRIS---GERADOR-DE-JSONs

# Ou baixe o ZIP e extraia
```

### Passo 2: Instale as Dependências

```bash
pip install -r requirements.txt
```

**Isso pode levar 1-2 minutos** (estão sendo baixadas do internet)

### Passo 3: Execute a Aplicação

**Windows:**
```bash
executar_app.bat
```

**Mac/Linux:**
```bash
streamlit run src/app_streamlit.py
```

A aplicação abrirá em: **http://localhost:8501** ✅

---

## 🆘 Problemas Comuns

### ❓ "Python command not found"

**Causa:** Python não está no PATH

**Solução Windows:**
1. Desinstale Python
2. Instale novamente
3. **MARQUE "Add Python to PATH"** durante instalação
4. Reinicie o computador

**Solução Mac/Linux:**
```bash
export PATH="/usr/local/bin:$PATH"
python3 --version
```

---

### ❓ "pip command not found"

**Solução:**
```bash
# Use:
python -m pip install -r requirements.txt

# Em vez de:
pip install -r requirements.txt
```

---

### ❓ "ModuleNotFoundError: No module named 'streamlit'"

**Solução:**
```bash
pip install --upgrade streamlit
```

Se ainda não funcionar:
```bash
python -m pip install --upgrade streamlit
```

---

### ❓ Executar em outra porta (8501 está ocupada)

**Solução:**
```bash
streamlit run src/app_streamlit.py --server.port 8502
```

---

### ❓ Permissão negada no Mac/Linux

**Solução:**
```bash
chmod +x executar_app.sh
./executar_app.sh
```

---

## 🔍 Verificar Instalação Completa

Execute este comando para verificar tudo:

```bash
python -c "import sys; print(f'Python {sys.version}'); import streamlit; print('✓ Streamlit OK')"
```

Se ver algo como abaixo, está tudo certo:

```
Python 3.11.7 (main, ...)
✓ Streamlit OK
```

---

## 📊 Versões Recomendadas

| Componente | Versão Mínima | Versão Recomendada | Máxima Suportada |
|-----------|------|-----------|---------|
| **Python** | 3.7 | 3.11 | 3.12 |
| **Streamlit** | 1.28.0 | 1.28.0+ | Qualquer |
| **pip** | 20.0 | 23.0+ | Qualquer |

---

## 🚀 Próximos Passos

Após instalar Python com sucesso:

1. ✅ **Clonar repositório** (veja acima)
2. ✅ **Instalar dependências** (veja acima)
3. ✅ **Executar aplicação** (veja acima)
4. 📖 Ler [GUIA_RAPIDO.md](GUIA_RAPIDO.md) para aprender a usar

---

## 💡 Dicas

- **Não consegue instalar?** Tente o script `instalar_python.bat` primeiro
- **Está lento?** Use `python -m pip install --upgrade pip` para atualizar pip
- **Quer versão portável?** Use [Portable Python](https://www.portablepython.com/)
- **Ambiente corporativo?** Peça ao TI para instalar Python
- **Não quer instalar localmente?** Use [Replit](https://replit.com/) online gratuitamente

---

## 🤝 Precisa de Ajuda?

- 🐛 [Abra uma issue no GitHub](https://github.com/marcosfsense/AUTOMA--O-HYBRIS---GERADOR-DE-JSONs/issues)
- 💬 [Deixe um comentário](https://github.com/marcosfsense/AUTOMA--O-HYBRIS---GERADOR-DE-JSONs/discussions)
- 📧 Contate o desenvolvedor

---

**Desenvolvido para tornar a instalação o mais simples possível** 🎉
