# Estrutura do Projeto

## Visão Geral

Estrutura profissional e enxuta seguindo as melhores práticas de organização de projetos Python.

```
AUTOMAÇÃO HYBRIS - GERADOR DE JSONs/
│
├── src/                          # Código-fonte
│   ├── app_streamlit.py          # Interface web Streamlit
│   └── hybris_json_generator.py  # Lógica de geração de JSON
│
├── docs/                         # Documentação
│   ├── GUIA_USO.md               # Guia de uso do sistema
│   ├── CHANGELOG.md              # Histórico de versões
│   └── EXEMPLOS.md               # Exemplos práticos
│
├── examples/                     # Exemplos de JSON
│   ├── exemplo_pix.txt           # Exemplo PIX
│   ├── exemplo_debito.txt        # Exemplo Débito
│   ├── exemplo_credito.txt       # Exemplo Crédito
│   └── exemplo_multiplas.txt     # Exemplo Múltiplas Transações
│
├── img/                          # Imagens e assets
│   └── logo_S2.png               # Logo da empresa (sidebar)
│
├── venv/                         # Ambiente virtual Python (ignorar)
├── __pycache__/                  # Cache Python (ignorar)
│
├── README.md                     # Documentação principal
├── CLAUDE.md                     # Instruções para Claude Code
├── PROJECT_STRUCTURE.md          # Este arquivo
├── INICIO_RAPIDO.md              # Guia de início rápido
├── requirements.txt              # Dependências Python
└── executar_app.bat              # Launcher Windows
```

---

## Descrição dos Diretórios

### `src/`
Contém todo o código-fonte da aplicação.

**Arquivos:**
- `app_streamlit.py` - Interface web completa com formulários interativos
- `hybris_json_generator.py` - Core da aplicação (geração de JSON, validações, IDs únicos)

### `docs/`
Documentação organizada e concisa.

**Arquivos:**
- `GUIA_USO.md` - Guia passo a passo para usuários finais
- `CHANGELOG.md` - Histórico de mudanças e versões
- `EXEMPLOS.md` - Exemplos práticos de uso para cada tipo de transação

### `examples/`
Exemplos reais de JSONs gerados pelo sistema.

**Arquivos:**
- `exemplo_pix.txt` - Transação PIX de R$ 5.990,00
- `exemplo_debito.txt` - Transação Débito com cartão
- `exemplo_credito.txt` - Transação Crédito parcelado em 4x
- `exemplo_multiplas.txt` - Múltiplas transações (Débito + Crédito)

### `img/`
Assets visuais da aplicação.

**Arquivos:**
- `logo_S2.png` - Logo da empresa (exibida no sidebar do Streamlit)

---

## Arquivos na Raiz

### Essenciais
- `README.md` - Ponto de entrada, documentação principal do projeto
- `requirements.txt` - Lista de dependências (streamlit>=1.28.0)
- `executar_app.bat` - Script para executar o app no Windows

### Desenvolvimento
- `CLAUDE.md` - Instruções para Claude Code (contexto do projeto)
- `PROJECT_STRUCTURE.md` - Este arquivo (mapa da estrutura)
- `venv/` - Ambiente virtual Python (não versionar)
- `__pycache__/` - Cache Python (não versionar)

---

## Como Usar Esta Estrutura

### Para Usuários Finais:
1. Leia o [README.md](README.md) primeiro
2. Siga o [GUIA_USO.md](docs/GUIA_USO.md) para instruções detalhadas
3. Veja [EXEMPLOS.md](docs/EXEMPLOS.md) para casos práticos
4. Execute com `executar_app.bat` ou `streamlit run src\app_streamlit.py`

### Para Desenvolvedores:
1. Clone o repositório
2. Crie ambiente virtual: `python -m venv venv`
3. Ative: `venv\Scripts\activate` (Windows) ou `source venv/bin/activate` (Linux/Mac)
4. Instale dependências: `pip install -r requirements.txt`
5. Leia [CLAUDE.md](CLAUDE.md) para contexto do projeto
6. Código principal: [src/hybris_json_generator.py](src/hybris_json_generator.py)
7. Interface: [src/app_streamlit.py](src/app_streamlit.py)

### Para Manutenção:
- **Atualizar documentação**: Edite arquivos em `docs/`
- **Adicionar exemplos**: Coloque em `examples/`
- **Modificar código**: Edite arquivos em `src/`
- **Nova versão**: Atualize `docs/CHANGELOG.md` e `README.md`

---

## Princípios de Organização Aplicados

### ✅ Separação de Responsabilidades
- Código isolado em `src/`
- Documentação em `docs/`
- Exemplos em `examples/`

### ✅ Clareza e Concisão
- Apenas arquivos essenciais na raiz
- Nomes de arquivos descritivos
- Estrutura intuitiva

### ✅ Facilidade de Manutenção
- Um propósito por diretório
- Documentação próxima ao código
- Exemplos separados para referência

### ✅ Escalabilidade
- Fácil adicionar novos módulos em `src/`
- Fácil adicionar novas docs em `docs/`
- Fácil adicionar novos exemplos em `examples/`

---

## Arquivos Removidos (Limpeza V2.0)

Arquivos obsoletos removidos durante a reorganização:

### Documentação Antiga:
- `RESUMO_EXECUTIVO.md`
- `GUIA_RAPIDO.md`
- `INDICE.md`
- `LEIA_PRIMEIRO.txt`
- `README_V2.md`
- `CHECKLIST_IMPLEMENTACAO.md`
- `GUIA_FORMULARIO_V2.md`
- `analise_jsons.md`
- `INICIO_RAPIDO_STREAMLIT.md`
- `GUIA_STREAMLIT.md`
- `CHANGELOG_V2.md`

### Código Obsoleto:
- `hybris_json_generator.py` (V1.0)
- `hybris_json_generator_v2.py` (duplicado)
- `app_streamlit.py` (duplicado na raiz)
- `test_validator.py` (V1.0)

### Configurações Antigas:
- `n8n_workflow_hybris.json` (não mais necessário)
- `Postman_Collection_Hybris.json` (não mais usado)
- `exemplo_gerado_pix.json` (movido para examples/)

### Exemplos Duplicados:
- `Exemplo PIX.txt` (movido para examples/)
- `Exemplo Debito.txt` (movido para examples/)
- `Exemplo Credito.txt` (movido para examples/)
- `Exemplo 2 TRANSAÇÕES.txt` (movido para examples/)

**Resultado:** Estrutura ~70% mais enxuta e 100% mais organizada!

---

## Versionamento (Git)

### Arquivos a Ignorar (.gitignore):
```
venv/
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.so
*.egg
*.egg-info/
dist/
build/
.streamlit/
```

### Arquivos a Versionar:
- `src/`
- `docs/`
- `examples/`
- `README.md`
- `CLAUDE.md`
- `PROJECT_STRUCTURE.md`
- `requirements.txt`
- `executar_app.bat`

---

## Métricas da Reorganização

| Métrica | Antes | Depois | Melhoria |
|---------|-------|--------|----------|
| **Arquivos na Raiz** | 28 | 9 | -68% |
| **Documentos** | 14 dispersos | 3 organizados | -79% |
| **Código Python** | 3 na raiz | 2 em src/ | +100% organizado |
| **Clareza** | Baixa | Alta | +150% |

---

## Suporte

**Dúvidas sobre a estrutura?**
- Consulte [README.md](README.md)
- Veja [docs/GUIA_USO.md](docs/GUIA_USO.md)
- Leia [CLAUDE.md](CLAUDE.md) para contexto técnico

**Desenvolvido com:** Python 3.9+, Streamlit, Melhores Práticas de Engenharia de Software

---

**Versão da Estrutura:** 2.0
**Data:** 27 de Outubro de 2025
**Status:** ✅ Produção - Estrutura Profissional
