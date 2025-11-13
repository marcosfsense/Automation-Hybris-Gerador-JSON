# 📝 Guia Completo: Explicação Linha-a-Linha do app_streamlit.py

> Documentação detalhada de cada seção do código da aplicação Streamlit

---

## 📋 Índice Rápido

- [Imports](#imports)
- [Configuração da Página](#configuração-da-página)
- [Estilos CSS](#estilos-css)
- [Sidebar](#sidebar)
- [Formulário Principal](#formulário-principal)
- [Tipos de Transação](#tipos-de-transação)
- [Processamento JSON](#processamento-json)

---

## IMPORTS

```python
import streamlit as st              # Framework web para criar a interface
import json                         # Biblioteca para manipular JSON
import os                           # Funções do sistema operacional
from pathlib import Path            # Trabalhar com caminhos de arquivos
from hybris_json_generator import HybrisJSONGenerator  # Classe geradora
```

### Explicação:

| Biblioteca | Uso |
|-----------|-----|
| **streamlit** | Cria a interface web interativa |
| **json** | Parse e manipulação de JSON |
| **os** | Acesso a variáveis do sistema |
| **Path** | Trabalhar com caminhos de forma multiplataforma (Windows/Mac/Linux) |
| **HybrisJSONGenerator** | Classe que gera os JSONs validados |

---

## Configuração da Página

```python
st.set_page_config(
    page_title="Gerador JSON Hybris",    # Aparece na aba do navegador
    page_icon="🚀",                      # Ícone da aba
    layout="wide",                       # Layout largura completa (sem margens)
    initial_sidebar_state="expanded"     # Sidebar aberta ao iniciar
)
```

### O que cada parâmetro faz:

| Parâmetro | Efeito |
|-----------|--------|
| `page_title` | Muda o título que aparece na aba do navegador |
| `page_icon` | Muda o ícone que aparece na aba |
| `layout="wide"` | Usa toda a largura da tela (sem bordas laterais) |
| `initial_sidebar_state="expanded"` | Abre a barra lateral automaticamente |

---

## Estilos CSS

```python
st.markdown("""<style>
    .main-header {
        font-size: 2.5rem;          # Tamanho do texto (muito grande)
        color: #1f77b4;             # Cor azul em hexadecimal
        text-align: center;         # Centraliza na página
        margin-bottom: 2rem;        # Espaço embaixo
    }
    .success-box {                  # Caixa verde (sucesso)
        background-color: #d4edda;  # Fundo verde claro
        border: 1px solid #c3e6cb;  # Borda verde
        color: #155724;             # Texto verde escuro
    }
    .error-box {                    # Caixa vermelha (erro)
        background-color: #f8d7da;  # Fundo vermelho claro
        border: 1px solid #f5c6cb;  # Borda vermelha
        color: #721c24;             # Texto vermelho escuro
    }
    .info-box {                     # Caixa azul (informação)
        background-color: #d1ecf1;  # Fundo azul claro
        border: 1px solid #bee5eb;  # Borda azul
        color: #0c5460;             # Texto azul escuro
    }
</style>""", unsafe_allow_html=True)
```

### O que faz:

Define estilos visuais para diferentes tipos de mensagens:
- ✅ **success-box** - Sucesso (verde)
- ❌ **error-box** - Erro (vermelho)
- ℹ️ **info-box** - Informação (azul)

---

## Sidebar

```python
with st.sidebar:                # Cria seção na barra lateral esquerda
    # Carrega e exibe a logo
    logo_path = Path(__file__).parent.parent / "img" / "logo_S2.png"
    # Path(__file__) = Arquivo atual (app_streamlit.py)
    # .parent = Pasta pai (src/)
    # .parent = Pasta pai da pasta pai (raiz do projeto)
    # / "img" / "logo_S2.png" = Caminho até a imagem

    if logo_path.exists():      # Verifica se a imagem existe
        st.image(str(logo_path), width='stretch')  # Exibe a imagem
        st.markdown("---")      # Linha de separação

    st.header("📋 Instruções")  # Título na sidebar

    # Texto com instruções em Markdown
    st.markdown("""
    ### Como usar:
    1. **Cole o JSON do cabeçalho**
    2. **Selecione o tipo** de transação
    3. **Preencha os campos** específicos
    4. **Clique em "Gerar JSON"**
    5. **Copie o resultado** para usar no Postman
    """)

    # Caixa de informação com versão
    st.info("**Versão:** 2.0\n\n**Status:** Operacional ✅")
```

### Estrutura:
- 📷 Exibe logo da empresa
- 📖 Mostra instruções de uso
- 📊 Mostra informações da aplicação

---

## Formulário Principal

### Seção 1: JSON do Cabeçalho

```python
st.subheader("1️⃣ JSON do Cabeçalho (do Hybris)")
# Cria um subtítulo na página

st.info("ℹ️ Cole TODO o JSON até ANTES de \"transactions\"")
# Mostra uma caixa azul com informação importante

header_json_str = st.text_area(
    "Cole aqui o JSON do cabeçalho do pedido:",
    height=300,                 # Altura do campo em pixels
    placeholder="{...}",        # Texto cinza que aparece vazio
    help="Cole até antes de 'transactions'"  # Dica ao passar mouse
)
# Retorna o texto digitado pelo usuário como string
```

### Seção 2: Tipo de Transação

```python
transaction_type = st.selectbox(
    "Selecione o tipo de transação:",
    ["", "PIX", "DEBITO", "CREDITO", "MULTIPLAS"],  # Opções
    help="Escolha o tipo de pagamento"
)
# Retorna a opção selecionada como string
```

### Seção 2.1: Pré-preenchimento

```python
# Armazena dados na memória da sessão (persiste enquanto app roda)
if 'prefill_data' not in st.session_state:
    st.session_state.prefill_data = None

# Radio button (botão de seleção única)
has_existing_transaction = st.radio(
    "Já existe a transação?",
    ["Não", "Sim"],
    help="Se já tem o JSON, pode colar aqui"
)

if has_existing_transaction == "Sim":
    existing_transactions_str = st.text_area(
        "Cole o JSON das transações existentes:",
        height=200
    )

    # Tenta fazer parse (converter) do JSON
    try:
        parsed = json.loads(existing_transactions_str.strip())

        # Se for um objeto com "transactions", extrai
        if isinstance(parsed, dict) and "transactions" in parsed:
            prefill_data = parsed["transactions"]
        # Se já for um array, usa diretamente
        elif isinstance(parsed, list):
            prefill_data = parsed

        # Se conseguiu fazer parse, mostra sucesso
        if prefill_data:
            st.success(f"✅ {len(prefill_data)} transação(ões) detectada(s)!")

    # Se o JSON é inválido, mostra erro
    except json.JSONDecodeError as e:
        st.error(f"❌ Erro: {str(e)}")
```

---

## Tipos de Transação

### PIX

```python
if transaction_type == "PIX":
    # Cria 2 colunas lado a lado
    col1, col2 = st.columns(2)

    with col1:  # Primeira coluna
        pix_amount = st.number_input(
            "amount *",
            min_value=0.01,     # Mínimo permitido
            value=0.01,         # Valor inicial
            step=0.01,          # Incremento/decremento
            format="%.2f"       # Formato: 2 casas decimais
        )
        # Retorna um número float

        pix_number = st.text_input(
            "number *",
            help="Número da transação/terminal"
        )
        # Retorna um texto/string

    with col2:  # Segunda coluna
        pix_merchant_name = st.text_input(
            "merchantName *",
            value="Fake callback Bruno - ",
            help="Nome do estabelecimento"
        )

        pix_auth_code = st.text_input(
            "authorization_code (opcional)",
            help="Deixe em branco para gerar automaticamente"
        )

    # Botão para gerar o JSON
    if st.button("🚀 Gerar JSON", type="primary"):
        # Verifica se campos obrigatórios estão preenchidos
        if not pix_number or not pix_merchant_name:
            st.error("❌ Preencha todos os campos!")
        else:
            # Prepara dados para enviar ao gerador
            trans_data = {
                "amount": pix_amount,
                "number": pix_number,
                "merchant_name": pix_merchant_name,
                "authorization_code": pix_auth_code if pix_auth_code else None
            }
            transactions_data = [trans_data]
```

### DÉBITO

Similar ao PIX, mas com campos adicionais:

```python
if transaction_type == "DEBITO":
    # ... campos de amount, number, merchant_name ...

    deb_auth_code = st.text_input(
        "authorization_code *",     # Obrigatório para débito
        help="Código de autorização do banco"
    )

    # Dados para transação de débito
    trans_data = {
        "amount": deb_amount,
        "number": deb_number,
        "merchant_name": deb_merchant_name,
        "card_mask": "************XXXX",      # Máscara do cartão (hardcoded)
        "card_brand": "XXXXXXXX",             # Marca do cartão (hardcoded)
        "authorization_code": deb_auth_code
    }
```

### CRÉDITO

Igual ao débito, mas com parcelas:

```python
if transaction_type == "CREDITO":
    # ... campos de amount, number, merchant_name ...

    cred_quotas = st.number_input(
        "numberOfQuotas *",
        min_value=1,        # Mínimo 1 parcela
        max_value=24,       # Máximo 24 parcelas
        value=1             # Padrão 1
    )

    # Dados incluem parcelas
    trans_data = {
        "amount": cred_amount,
        "number": cred_number,
        "merchant_name": cred_merchant_name,
        "number_of_quotas": int(cred_quotas),  # Converte para inteiro
        "card_mask": "************XXXX",
        "card_brand": "XXXXXXXX",
        "authorization_code": cred_auth_code
    }
```

### MÚLTIPLAS TRANSAÇÕES

```python
elif transaction_type == "MULTIPLAS":
    # Input para número de transações
    num_transactions = st.number_input(
        "Quantas transações?",
        min_value=2,        # Mínimo 2 para "múltiplas"
        max_value=5,        # Máximo 5
        value=2
    )

    # Cria abas (tabs) - uma para cada transação
    tabs = st.tabs([f"Transação {i+1}" for i in range(int(num_transactions))])
    # Exemplo: ["Transação 1", "Transação 2", "Transação 3"]

    temp_transactions = []

    # Itera sobre cada aba
    for idx, tab in enumerate(tabs):  # idx = índice (0, 1, 2...)
        with tab:  # Entra na aba atual
            st.markdown(f"### Transação {idx+1}")

            # Detecta o tipo da transação anterior (se tiver pré-preenchimento)
            if prefill_data and idx < len(prefill_data):
                prefill_trans = prefill_data[idx]

                # Extrai o product code para detectar tipo
                product_code = prefill_trans["payment_fields"].get("primaryProductCode", 25)
                if product_code == 25:
                    detected_type = "PIX"
                elif product_code == 2000:
                    detected_type = "DEBITO"
                elif product_code == 1000:
                    detected_type = "CREDITO"

            # Selectbox para escolher tipo
            trans_type = st.selectbox(
                f"Tipo",
                ["PIX", "DEBITO", "CREDITO"],
                key=f"type_{idx}"  # key único para cada transação
            )

            # ... Campos específicos para cada tipo ...

            # Adiciona à lista de transações
            temp_transactions.append(trans_data)

    # Botão para gerar JSON com todas as transações
    if st.button("🚀 Gerar JSON", type="primary"):
        # Valida cada transação
        all_valid = True
        for i, trans in enumerate(temp_transactions):
            if not trans.get("number") or not trans.get("merchant_name"):
                st.error(f"⚠️ Transação {i+1}: Preencha todos os campos!")
                all_valid = False

        if all_valid:
            transactions_data = temp_transactions
```

---

## Processamento JSON

```python
# Só processa se houver dados de transação
if transactions_data:
    st.markdown("---")  # Linha de separação
    st.subheader("4️⃣ Resultado")

    try:
        # Verifica se cabeçalho foi preenchido
        if not header_json_str.strip():
            st.error("❌ Cole o JSON do cabeçalho!")
        else:
            # Limpa o JSON (remove vírgula final)
            cleaned_json = header_json_str.strip()

            if not cleaned_json.endswith('}'):
                if cleaned_json.endswith(','):
                    cleaned_json = cleaned_json.rstrip(',').rstrip()
                cleaned_json += '\n}'

            # Parse (converte string JSON em objeto Python)
            header_json = json.loads(cleaned_json)

            # Cria instância do gerador
            generator = HybrisJSONGenerator()

            # Gera o JSON completo
            result = generator.generate_json_with_header(
                header_json=header_json,
                transaction_type=transaction_type,
                transactions_data=transactions_data
            )

            # Verifica se houve erro na validação
            if isinstance(result, dict) and not result.get("success", True):
                # Mostra cada erro encontrado
                for error in result.get("validation_errors", []):
                    st.error(f"  • {error}")
            else:
                # Parse do resultado (string JSON → objeto)
                result_obj = json.loads(result)

                # Mostra sucesso
                st.success("✅ JSON gerado com sucesso!")

                # Mostra métricas em 3 colunas
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Número do Pedido", result_obj["number"])
                with col2:
                    st.metric("Total de Transações", len(result_obj["transactions"]))
                with col3:
                    # Converte centavos para reais (divide por 100)
                    st.metric("Valor Total", f"R$ {result_obj['price']/100:.2f}")

                # Exibe o JSON formatado
                st.markdown("### 📄 JSON Gerado:")
                st.code(result, language="json", line_numbers=True)
                # language="json" → colore como JSON
                # line_numbers=True → mostra números de linha

                # Botão para baixar o JSON
                st.download_button(
                    label="📥 Baixar JSON",
                    data=result,                            # Conteúdo do arquivo
                    file_name=f"hybris_{result_obj['number']}.json",  # Nome do arquivo
                    mime="application/json",                # Tipo de arquivo
                    use_container_width=True                # Botão ocupa toda largura
                )

                # Informação sobre próximos passos
                st.info("💡 Use o JSON no Postman para enviar à API Hybris.")

    # Se JSON do cabeçalho for inválido
    except json.JSONDecodeError as e:
        st.error(f"❌ Erro no JSON do cabeçalho: {str(e)}")

    # Qualquer outro erro
    except Exception as e:
        st.error(f"❌ Erro: {str(e)}")
        st.exception(e)  # Mostra traceback completo
```

---

## Footer

```python
st.markdown("---")  # Linha de separação

# HTML customizado para rodapé
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem 0;">
    <p><strong>Gerador de JSON (Fake Callback) -  Hybris</strong></p>
    <p>Versão 2.0 | Desenvolvido para automação de vinculação de pagamentos</p>
</div>
""", unsafe_allow_html=True)
```

---

## Resumo de Conceitos Importantes

### Session State
```python
# Armazena dados entre cliques do usuário
st.session_state.prefill_data = data
# Persiste enquanto a aplicação está rodando
```

### Widgets Interativos
```python
st.text_input()      # Campo de texto
st.number_input()    # Campo de número
st.selectbox()       # Dropdown de seleção
st.radio()          # Botões de seleção única
st.button()         # Botão clicável
st.text_area()      # Área de texto grande
st.columns()        # Cria colunas lado a lado
st.tabs()           # Cria abas
```

### Exibição de Informações
```python
st.write()          # Escreve qualquer coisa
st.markdown()       # Escreve em Markdown ou HTML
st.code()           # Mostra código com sintaxe colorida
st.json()           # Mostra JSON formatado
st.info()           # Caixa azul de informação
st.success()        # Caixa verde de sucesso
st.warning()        # Caixa amarela de aviso
st.error()          # Caixa vermelha de erro
st.metric()         # Mostra uma métrica com número grande
st.image()          # Exibe imagem
st.download_button()# Botão para baixar arquivo
```

### Fluxo de Controle
```python
# Condicional baseado em seleção
if transaction_type == "PIX":
    # Mostra campos específicos para PIX
elif transaction_type == "DEBITO":
    # Mostra campos específicos para Débito

# Condicional baseado em clique
if st.button("Gerar"):
    # Executa apenas quando clicado

# Contexto de coluna
with col1:
    # Todos os widgets aqui ficam na coluna 1

# Contexto de aba
with tab:
    # Todos os widgets aqui ficam nesta aba
```

---

**Desenvolvido para facilitar o entendimento do código da aplicação Streamlit** 🚀
