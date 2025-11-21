"""
Aplicativo Streamlit - Gerador de JSONs Hybris
Versão 2.0 - Interface Web Completa

Executar com: streamlit run app_streamlit.py
"""

# ═══════════════════════════════════════════════════════════════════════
# IMPORTS - Importações necessárias para o funcionamento
# ═══════════════════════════════════════════════════════════════════════

import streamlit as st              # Framework web para criar a interface
import json                         # Biblioteca para manipular JSON
import os                           # Funções do sistema operacional
from pathlib import Path            # Trabalhar com caminhos de arquivos
from hybris_json_generator import HybrisJSONGenerator  # Classe geradora do JSON

# ═══════════════════════════════════════════════════════════════════════
# FUNÇÃO HELPER - Extrair transação de diferentes formatos Hybris
# ═══════════════════════════════════════════════════════════════════════

def normalize_amount_from_json(amount_value) -> float:
    """
    Normaliza o amount para Reais quando vem do JSON (centavos).

    O Hybris sempre envia amount em centavos (inteiro).
    O app trabalha com Reais (decimal).

    Args:
        amount_value: Valor em centavos (int) ou já em Reais (float)

    Returns:
        Valor normalizado em Reais (float)
    """
    if amount_value is None:
        return 0.0

    # Se for inteiro > 100, provavelmente é centavos (ex: 284050 = R$ 2840.50)
    # Se for inteiro < 100 ou float, provavelmente já é Reais
    if isinstance(amount_value, int):
        if amount_value > 100:
            # Converter centavos para Reais
            return amount_value / 100
        else:
            # Pequeno valor em centavos ou outra unidade
            return float(amount_value)
    elif isinstance(amount_value, float):
        # Já é float, provavelmente em Reais
        return amount_value
    else:
        # Tentar converter string
        try:
            val = float(amount_value)
            if val > 100:
                return val / 100
            return val
        except (ValueError, TypeError):
            return 0.0


def extract_transaction_from_hybris(data: dict) -> dict:
    """
    Extrai a transação de diferentes formatos que o Hybris pode retornar.

    Inteligentemente detecta e navega por múltiplos níveis de aninhamento,
    suportando diversos formatos de resposta da API Hybris.

    Suporta:
    1. Objeto direto: { "id": "...", "amount": ... }
    2. Com chave "transaction": { "transaction": { "id": "...", ... } }
    3. Com chave "trasaction" (typo): { "trasaction": { "id": "...", ... } }
    4. Com chave "transactions" (array): { "transactions": [{ "id": "...", ... }] }
    5. Aninhado com order: { "id": "order", "trasaction": { "id": "trans", ... } }
    6. Múltiplos campos + transação: { "id": "...", "order_id": "...", "transactions": [...] }

    Args:
        data: Dict com a transação em qualquer formato

    Returns:
        Dict com a transação extraída, ou Dict vazio se não encontrar
    """
    # Estratégia 1: Se for um objeto direto com "id" e "amount", retornar como está
    # (indica que é a transação própria)
    if data.get("id") and data.get("amount"):
        return data

    # Estratégia 2: Procurar por chaves conhecidas de transação (em ordem de prioridade)
    transaction_keys = ["transaction", "trasaction", "transactions"]

    for key in transaction_keys:
        if key in data:
            value = data[key]

            # Se for um dict direto, retornar
            if isinstance(value, dict):
                # Verificar se é a transação ou se precisa descer mais
                if value.get("id") and value.get("amount"):
                    return value
                # Se não tem amount, pode estar em outro nível (improvável mas seguro)
                return value

            # Se for um array, pegar o primeiro elemento
            if isinstance(value, (list, tuple)) and len(value) > 0:
                first_item = value[0]
                if isinstance(first_item, dict):
                    if first_item.get("id") and first_item.get("amount"):
                        return first_item
                    return first_item

    # Estratégia 3: Se não encontrou nas chaves conhecidas, procurar recursivamente
    # por um objeto que tem "id" e "amount" em qualquer nível
    for key, value in data.items():
        if isinstance(value, dict):
            # Tentar extrair recursivamente
            if value.get("id") and value.get("amount"):
                return value

            # Se for um array, tentar o primeiro elemento
            if isinstance(value, (list, tuple)) and len(value) > 0:
                first_item = value[0]
                if isinstance(first_item, dict) and first_item.get("id") and first_item.get("amount"):
                    return first_item

    # Estratégia 4: Se o objeto tem muitos campos mas não tem "amount",
    # procurar por "amount" dentro de sub-objetos
    for key, value in data.items():
        if isinstance(value, dict) and value.get("amount"):
            return value

    # Se nada encontrar, retornar o original
    # (pode ser que já seja a transação correta mesmo sem amount no nível superior)
    return data

# ═══════════════════════════════════════════════════════════════════════
# CONFIGURAÇÃO DA PÁGINA - Personalizações do Streamlit
# ═══════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Gerador JSON Hybris",   # Título que aparece na aba do navegador
    page_icon="🚀",                     # Ícone da aba
    layout="wide",                      # Layout largo (sem bordas laterais)
    initial_sidebar_state="expanded"    # Sidebar começa expandida
)

# ═══════════════════════════════════════════════════════════════════════
# CSS CUSTOMIZADO - Estilos visuais para a aplicação
# ═══════════════════════════════════════════════════════════════════════

st.markdown("""
<style>
    # Estilos para o cabeçalho principal
    .main-header {
        font-size: 2.5rem;              # Tamanho grande do texto
        color: #1f77b4;                 # Cor azul
        text-align: center;             # Centralizar
        margin-bottom: 2rem;            # Espaço embaixo
    }

    # Estilos para caixa de sucesso (verde)
    .success-box {
        padding: 1rem;                  # Espaço interno
        background-color: #d4edda;      # Fundo verde claro
        border: 1px solid #c3e6cb;      # Borda verde
        border-radius: 0.25rem;         # Cantos ligeiramente arredondados
        color: #155724;                 # Texto verde escuro
    }

    # Estilos para caixa de erro (vermelho)
    .error-box {
        padding: 1rem;
        background-color: #f8d7da;      # Fundo vermelho claro
        border: 1px solid #f5c6cb;      # Borda vermelha
        border-radius: 0.25rem;
        color: #721c24;                 # Texto vermelho escuro
    }

    # Estilos para caixa de informação (azul)
    .info-box {
        padding: 1rem;
        background-color: #d1ecf1;      # Fundo azul claro
        border: 1px solid #bee5eb;      # Borda azul
        border-radius: 0.25rem;
        color: #0c5460;                 # Texto azul escuro
    }
</style>
""", unsafe_allow_html=True)  # unsafe_allow_html=True permite usar HTML/CSS puro

# ═══════════════════════════════════════════════════════════════════════
# TÍTULO PRINCIPAL - Cabeçalho da aplicação
# ═══════════════════════════════════════════════════════════════════════

# Renderiza o título usando a classe CSS "main-header" definida acima
st.markdown('<h1 class="main-header">🚀 Gerador de JSON (Fake Callback) -  Hybris</h1>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════
# SIDEBAR - Barra lateral com instruções e informações
# ═══════════════════════════════════════════════════════════════════════

# O contexto "with st.sidebar:" cria uma área na barra lateral esquerda
with st.sidebar:
    # Logo da empresa
    logo_path = Path(__file__).parent.parent / "img" / "logo_S2.png"
    if logo_path.exists():
        st.image(str(logo_path), width='stretch')
        st.markdown("---")

    st.header("📋 Instruções")
    st.markdown("""
    ### Como usar:

    1. **Cole o JSON do cabeçalho** obtido no Hybris
    2. **Selecione o tipo** de transação
    3. **Preencha os campos** específicos
    4. **Clique em "Gerar JSON"**
    5. **Copie o resultado** para usar no Postman

    ---

    ### Tipos de Transação:
    - **PIX**: Pagamento instantâneo
    - **DÉBITO**: Cartão de débito
    - **CRÉDITO**: Cartão de crédito (parcelado)
    - **MÚLTIPLAS**: Combinação de pagamentos

    ---

    ### Suporte:
    - Em caso de dúvida, consulte a documentação
    - Todos os IDs são gerados automaticamente
    - Timestamps usam timezone do Brasil
    """)

    st.info("**Versão:** 2.0\n\n**Status:** Operacional ✅")

# Área principal do formulário
st.markdown("---")

# SEÇÃO 1: JSON DO CABEÇALHO
st.subheader("1️⃣ JSON do Cabeçalho (do Hybris)")

st.info("ℹ️ **Importante:** Cole TODO o JSON do pedido ATÉ ANTES do campo `\"transactions\"`. Pode terminar com vírgula - o sistema corrige automaticamente.")

header_json_str = st.text_area(
    "Cole aqui o JSON do cabeçalho do pedido (até antes de 'transactions'):",
    height=300,
    placeholder="""{
  "id": "c777434f-a679-4298-9803-12d069a4a13d",
  "items": [{
    "id": 1186914740,
    "sku": "08389316",
    "name": "Leandro teixeira Filipe",
    "uuid": "fedcb39b-09d9-4951-9415-8b5a88522662",
    "details": null,
    "order_id": 3741538564,
    "quantity": 1,
    "created_at": "2022-09-09T14:58:12Z",
    "unit_price": 599000,
    "updated_at": "2022-09-09T14:58:12Z",
    ...
  }],
  "price": 599000,
  "number": "08389316",
  "status": "PAID",
  "reference": "Leandro teixeira Filipe",
  "created_at": "2022-09-09T14:58:12Z",
  "updated_at": "2022-09-09T14:58:12Z",

OU (com vírgula no final também funciona):
  ...
  "updated_at": "2022-09-09T14:58:12Z",
""",
    help="Cole até antes de 'transactions'. Pode ter vírgula no final - o sistema corrige."
)

st.markdown("---")

# SEÇÃO 2: TIPO DE TRANSAÇÃO
st.subheader("2️⃣ Tipo de Transação")

transaction_type = st.selectbox(
    "Selecione o tipo de transação:",
    ["", "PIX", "DEBITO", "CREDITO", "MULTIPLAS"],
    help="Escolha o tipo de pagamento que será vinculado"
)

st.markdown("---")

# Inicializar variáveis
transactions_data = []
result_json = None
error_message = None
prefill_data = None  # Inicializar prefill_data (removida seção 2.1)

# SEÇÃO 3: CAMPOS ESPECÍFICOS POR TIPO
if transaction_type:
    st.subheader(f"3️⃣ Dados da Transação - {transaction_type}")

    # ==================== PIX ====================
    if transaction_type == "PIX":
        # Pergunta: Já existe a transação?
        pix_has_existing = st.radio(
            "Já existe a transação?",
            ["Não", "Sim"],
            index=0,
            help="Se você já tem o JSON desta transação, pode colar aqui",
            key="pix_has_existing"
        )

        # Extrair dados de pré-preenchimento se existirem
        prefill_pix = None
        if prefill_data and len(prefill_data) > 0:
            prefill_pix = prefill_data[0]

        # ========== BLOCO: SIM (Apenas JSON) ==========
        if pix_has_existing == "Sim":
            st.info("ℹ️ Cole o JSON desta transação específica.")

            pix_json_str = st.text_area(
                "Cole aqui o JSON da transação PIX:",
                height=200,
                placeholder="""{
  "amount": 284050,
  "number": "1111111",
  "status": "PAID",
  "payment_fields": {
    "merchantName": "Fake callback ",
    "primaryProductCode": 25
  }
}""",
                key="pix_json_input"
            )

            prefill_pix_json = None
            if pix_json_str.strip():
                try:
                    json_loaded = json.loads(pix_json_str.strip())
                    # Extrair transação de diferentes formatos Hybris
                    prefill_pix_json = extract_transaction_from_hybris(json_loaded)
                    # Normalizar amount: converter centavos para Reais se necessário
                    if prefill_pix_json and "amount" in prefill_pix_json:
                        prefill_pix_json["amount"] = normalize_amount_from_json(prefill_pix_json["amount"])
                    st.success("✅ Transação carregada com sucesso!")
                except json.JSONDecodeError as e:
                    st.error(f"❌ Erro ao fazer parse do JSON: {str(e)}")
                    prefill_pix_json = None

            trans_data = prefill_pix_json if prefill_pix_json else {}
            if trans_data:
                transactions_data = [trans_data]

        # ========== BLOCO: NÃO (Formulário Manual) ==========
        else:
            col1, col2 = st.columns(2)

            with col1:
                pix_amount = st.number_input(
                    "amount *",
                    min_value=0.01,
                    value=prefill_pix.get("amount", 0.0) / 100 if prefill_pix else 0.01,
                    step=0.01,
                    format="%.2f",
                    help="Valor da transação em Reais"
                )

                pix_number = st.text_input(
                    "number *",
                    value=prefill_pix.get("number", "") if prefill_pix else "",
                    help="Número da transação/terminal"
                )

            with col2:
                default_merchant = "Fake callback - "
                if prefill_pix and prefill_pix.get("payment_fields"):
                    default_merchant = prefill_pix["payment_fields"].get("merchantName", default_merchant)

                pix_merchant_name = st.text_input(
                    "merchantName *",
                    value=default_merchant,
                    help="Nome do estabelecimento comercial"
                )

                default_auth = ""
                if prefill_pix and prefill_pix.get("authorization_code"):
                    default_auth = prefill_pix["authorization_code"]

                pix_auth_code = st.text_input(
                    "authorization_code (opcional)",
                    value=default_auth,
                    help="Deixe em branco para gerar automaticamente"
                )

            # Preparar dados
            trans_data = {
                "amount": pix_amount,
                "number": pix_number,
                "merchant_name": pix_merchant_name,
                "authorization_code": pix_auth_code if pix_auth_code else None
            }
            # Preservar payment_fields originais se houver pré-preenchimento
            if prefill_pix and prefill_pix.get("payment_fields"):
                trans_data["preserve_payment_fields"] = prefill_pix["payment_fields"]

            transactions_data = [trans_data]

        # Botão para gerar
        if st.button("🚀 Gerar JSON", type="primary"):
            if pix_has_existing == "Sim":
                # JSON colado - validar apenas número
                if not transactions_data or not transactions_data[0].get("number"):
                    st.error("⚠️ JSON colado precisa ter 'number'!")
                else:
                    transactions_data = [transactions_data[0]]
            else:
                # Formulário manual - validar campos
                if not pix_number or not pix_merchant_name:
                    st.error("⚠️ Por favor, preencha todos os campos obrigatórios!")
                else:
                    transactions_data = [trans_data]

    # ==================== DÉBITO ====================
    elif transaction_type == "DEBITO":
        # Pergunta: Já existe a transação?
        deb_has_existing = st.radio(
            "Já existe a transação?",
            ["Não", "Sim"],
            index=0,
            help="Se você já tem o JSON desta transação, pode colar aqui",
            key="deb_has_existing"
        )

        # Extrair dados de pré-preenchimento se existirem
        prefill_deb = None
        if prefill_data and len(prefill_data) > 0:
            prefill_deb = prefill_data[0]

        # ========== BLOCO: SIM (Apenas JSON) ==========
        if deb_has_existing == "Sim":
            st.info("ℹ️ Cole o JSON desta transação específica.")

            deb_json_str = st.text_area(
                "Cole aqui o JSON da transação DÉBITO:",
                height=200,
                placeholder="""{
  "amount": 100000,
  "number": "1111111",
  "status": "CONFIRMED",
  "payment_fields": {
    "merchantName": "Fake callback ",
    "primaryProductCode": 2000,
    "authorization_code": "abc123"
  }
}""",
                key="deb_json_input"
            )

            prefill_deb_json = None
            if deb_json_str.strip():
                try:
                    json_loaded = json.loads(deb_json_str.strip())
                    # Extrair transação de diferentes formatos Hybris
                    prefill_deb_json = extract_transaction_from_hybris(json_loaded)
                    # Normalizar amount: converter centavos para Reais se necessário
                    if prefill_deb_json and "amount" in prefill_deb_json:
                        prefill_deb_json["amount"] = normalize_amount_from_json(prefill_deb_json["amount"])
                    st.success("✅ Transação carregada com sucesso!")
                except json.JSONDecodeError as e:
                    st.error(f"❌ Erro ao fazer parse do JSON: {str(e)}")
                    prefill_deb_json = None

            trans_data = prefill_deb_json if prefill_deb_json else {}
            if trans_data:
                transactions_data = [trans_data]

        # ========== BLOCO: NÃO (Formulário Manual) ==========
        else:
            col1, col2 = st.columns(2)

            with col1:
                deb_amount = st.number_input(
                    "amount *",
                    min_value=0.01,
                    value=prefill_deb.get("amount", 0.0) / 100 if prefill_deb else 0.01,
                    step=0.01,
                    format="%.2f"
                )

                deb_number = st.text_input(
                    "number *",
                    value=prefill_deb.get("number", "") if prefill_deb else ""
                )

            with col2:
                default_merchant = "Fake callback - "
                if prefill_deb and prefill_deb.get("payment_fields"):
                    default_merchant = prefill_deb["payment_fields"].get("merchantName", default_merchant)

                deb_merchant_name = st.text_input(
                    "merchantName *",
                    value=default_merchant
                )

                default_auth = ""
                if prefill_deb and prefill_deb.get("authorization_code"):
                    default_auth = prefill_deb["authorization_code"]

                deb_auth_code = st.text_input(
                    "authorization_code *",
                    value=default_auth
                )

            # Preparar dados
            trans_data = {
                "amount": deb_amount,
                "number": deb_number,
                "merchant_name": deb_merchant_name,
                "card_mask": "************XXXX",
                "card_brand": "XXXXXXXX",
                "authorization_code": deb_auth_code
            }
            # Preservar campos originais se houver pré-preenchimento
            if prefill_deb:
                if prefill_deb.get("payment_fields"):
                    trans_data["preserve_payment_fields"] = prefill_deb["payment_fields"]
                if prefill_deb.get("card"):
                    trans_data["preserve_card"] = prefill_deb["card"]
                if prefill_deb.get("external_id"):
                    trans_data["preserve_external_id"] = prefill_deb["external_id"]

            transactions_data = [trans_data]

        # Botão para gerar
        if st.button("🚀 Gerar JSON", type="primary"):
            if deb_has_existing == "Sim":
                # JSON colado - validar apenas número
                if not transactions_data or not transactions_data[0].get("number"):
                    st.error("⚠️ JSON colado precisa ter 'number'!")
                else:
                    transactions_data = [transactions_data[0]]
            else:
                # Formulário manual - validar campos
                if not all([deb_number, deb_merchant_name, deb_auth_code]):
                    st.error("⚠️ Por favor, preencha todos os campos obrigatórios!")
                else:
                    transactions_data = [trans_data]

    # ==================== CRÉDITO ====================
    elif transaction_type == "CREDITO":
        # Pergunta: Já existe a transação?
        cred_has_existing = st.radio(
            "Já existe a transação?",
            ["Não", "Sim"],
            index=0,
            help="Se você já tem o JSON desta transação, pode colar aqui",
            key="cred_has_existing"
        )

        # Extrair dados de pré-preenchimento se existirem
        prefill_cred = None
        if prefill_data and len(prefill_data) > 0:
            prefill_cred = prefill_data[0]

        # ========== BLOCO: SIM (Apenas JSON) ==========
        if cred_has_existing == "Sim":
            st.info("ℹ️ Cole o JSON desta transação específica.")

            cred_json_str = st.text_area(
                "Cole aqui o JSON da transação CRÉDITO:",
                height=200,
                placeholder="""{
  "amount": 240000,
  "number": "1111111",
  "status": "CONFIRMED",
  "payment_fields": {
    "merchantName": "Fake callback ",
    "primaryProductCode": 1000,
    "numberOfQuotas": 12,
    "authorization_code": "abc123"
  }
}""",
                key="cred_json_input"
            )

            prefill_cred_json = None
            if cred_json_str.strip():
                try:
                    json_loaded = json.loads(cred_json_str.strip())
                    # Extrair transação de diferentes formatos Hybris
                    prefill_cred_json = extract_transaction_from_hybris(json_loaded)
                    # Normalizar amount: converter centavos para Reais se necessário
                    if prefill_cred_json and "amount" in prefill_cred_json:
                        prefill_cred_json["amount"] = normalize_amount_from_json(prefill_cred_json["amount"])
                    st.success("✅ Transação carregada com sucesso!")
                except json.JSONDecodeError as e:
                    st.error(f"❌ Erro ao fazer parse do JSON: {str(e)}")
                    prefill_cred_json = None

            trans_data = prefill_cred_json if prefill_cred_json else {}
            if trans_data:
                transactions_data = [trans_data]

        # ========== BLOCO: NÃO (Formulário Manual) ==========
        else:
            col1, col2 = st.columns(2)

            with col1:
                cred_amount = st.number_input(
                    "amount *",
                    min_value=0.01,
                    value=prefill_cred.get("amount", 0.0) / 100 if prefill_cred else 0.01,
                    step=0.01,
                    format="%.2f"
                )

                cred_number = st.text_input(
                    "number *",
                    value=prefill_cred.get("number", "") if prefill_cred else ""
                )

                # Determinar valor padrão para numberOfQuotas
                # Opções: vazio (0) ou 1-24
                quotas_options = [""] + [str(i) for i in range(1, 25)]

                default_quotas_index = 0  # Vazio por padrão
                if prefill_cred and prefill_cred.get("payment_fields"):
                    quotas_from_prefill = prefill_cred["payment_fields"].get("numberOfQuotas")
                    if quotas_from_prefill and 1 <= quotas_from_prefill <= 24:
                        default_quotas_index = quotas_from_prefill

                cred_quotas_str = st.selectbox(
                    "numberOfQuotas *",
                    quotas_options,
                    index=default_quotas_index,
                    help="Selecione entre 1 e 24 parcelas"
                )

                # Converter para inteiro (0 se vazio)
                cred_quotas = int(cred_quotas_str) if cred_quotas_str else 0

            with col2:
                default_merchant = "Fake callback - "
                if prefill_cred and prefill_cred.get("payment_fields"):
                    default_merchant = prefill_cred["payment_fields"].get("merchantName", default_merchant)

                cred_merchant_name = st.text_input(
                    "merchantName *",
                    value=default_merchant
                )

                default_auth = ""
                if prefill_cred and prefill_cred.get("authorization_code"):
                    default_auth = prefill_cred["authorization_code"]

                cred_auth_code = st.text_input(
                    "authorization_code *",
                    value=default_auth
                )

            # Preparar dados
            trans_data = {
                "amount": cred_amount,
                "number": cred_number,
                "merchant_name": cred_merchant_name,
                "number_of_quotas": int(cred_quotas),
                "card_mask": "************XXXX",
                "card_brand": "XXXXXXXX",
                "authorization_code": cred_auth_code
            }
            # Preservar campos originais se houver pré-preenchimento
            if prefill_cred:
                if prefill_cred.get("payment_fields"):
                    trans_data["preserve_payment_fields"] = prefill_cred["payment_fields"]
                if prefill_cred.get("card"):
                    trans_data["preserve_card"] = prefill_cred["card"]
                if prefill_cred.get("external_id"):
                    trans_data["preserve_external_id"] = prefill_cred["external_id"]

            transactions_data = [trans_data]

        # Botão para gerar
        if st.button("🚀 Gerar JSON", type="primary"):
            if cred_has_existing == "Sim":
                # JSON colado - validar apenas número
                if not transactions_data or not transactions_data[0].get("number"):
                    st.error("⚠️ JSON colado precisa ter 'number'!")
                else:
                    transactions_data = [transactions_data[0]]
            else:
                # Formulário manual - validar campos
                if not all([cred_number, cred_merchant_name, cred_auth_code]) or cred_quotas == 0:
                    st.error("⚠️ Por favor, preencha todos os campos obrigatórios (incluindo numberOfQuotas)!")
                else:
                    transactions_data = [trans_data]

    # ==================== MÚLTIPLAS TRANSAÇÕES ====================
    elif transaction_type == "MULTIPLAS":
        st.info("ℹ️ Configure cada transação individualmente. A soma dos valores deve ser igual ao 'price' do cabeçalho.")

        # Determinar número de transações baseado em prefill_data ou input do usuário
        default_num_trans = len(prefill_data) if prefill_data else 2

        # Mostrar informação se foi detectado automaticamente
        if prefill_data and len(prefill_data) > 0:
            st.success(f"✅ Detectadas {len(prefill_data)} transações no JSON. Criando {len(prefill_data)} tabs automaticamente...")

        # Número de transações
        num_transactions = st.number_input(
            "Quantas transações?",
            min_value=2,
            max_value=10,
            value=default_num_trans,
            help="Ajuste se necessário. Valor pré-definido com base no JSON colado." if prefill_data else "Entre 2 e 10 transações"
        )

        # Usar session_state para armazenar dados das transações
        if 'multi_transactions' not in st.session_state:
            st.session_state.multi_transactions = []

        # Criar abas para cada transação
        tabs = st.tabs([f"Transação {i+1}" for i in range(int(num_transactions))])

        temp_transactions = []

        for idx, tab in enumerate(tabs):
            with tab:
                st.markdown(f"### Transação {idx+1}")

                # ========== PERGUNTA: JÁ EXISTE A TRANSAÇÃO? ==========
                has_existing_trans = st.radio(
                    "Já existe a transação?",
                    ["Não", "Sim"],
                    index=0,
                    help="Se você já tem o JSON desta transação, pode colar aqui",
                    key=f"has_existing_{idx}"
                )

                # Variável para armazenar dados extraídos da transação
                prefill_trans = None

                if has_existing_trans == "Sim":
                    st.info("ℹ️ Cole o JSON desta transação específica.")

                    existing_trans_str = st.text_area(
                        f"Cole aqui o JSON da transação {idx+1}:",
                        height=200,
                        placeholder="""{
  "amount": 284050,
  "number": "1111111",
  "status": "PAID",
  "payment_fields": {
    "merchantName": "Fake callback ",
    "authorization_code": "abc123"
  }
}""",
                        key=f"existing_trans_{idx}"
                    )

                    if existing_trans_str.strip():
                        try:
                            json_loaded = json.loads(existing_trans_str.strip())
                            # Extrair transação de diferentes formatos Hybris
                            prefill_trans = extract_transaction_from_hybris(json_loaded)
                            # Normalizar amount: converter centavos para Reais se necessário
                            if prefill_trans and "amount" in prefill_trans:
                                prefill_trans["amount"] = normalize_amount_from_json(prefill_trans["amount"])
                            st.success(f"✅ Transação {idx+1} carregada com sucesso!")
                        except json.JSONDecodeError as e:
                            st.error(f"❌ Erro ao fazer parse do JSON: {str(e)}")
                            prefill_trans = None

                    # Apenas preparar dados do JSON colado
                    trans_data = prefill_trans if prefill_trans else {}
                    if trans_data:
                        temp_transactions.append(trans_data)

                else:  # has_existing_trans == "Não"
                    # Mostrar formulário manual APENAS quando responder "Não"

                    # Extrair dados de pré-preenchimento para esta transação específica
                    if prefill_data and idx < len(prefill_data):
                        prefill_trans = prefill_data[idx]
                    else:
                        prefill_trans = None

                    detected_type = "PIX"  # Default

                    if prefill_trans and prefill_trans.get("payment_fields"):
                        product_code = prefill_trans["payment_fields"].get("primaryProductCode", 25)
                        if product_code == 25:
                            detected_type = "PIX"
                        elif product_code == 2000:
                            detected_type = "DEBITO"
                        elif product_code == 1000:
                            detected_type = "CREDITO"

                    # Selecionar tipo de transação
                    type_options = ["PIX", "DEBITO", "CREDITO"]
                    type_index = type_options.index(detected_type) if detected_type in type_options else 0

                    trans_type = st.selectbox(
                        f"Tipo",
                        type_options,
                        index=type_index,
                        key=f"type_{idx}"
                    )

                    col1, col2 = st.columns(2)

                    with col1:
                        default_amount = 0.01
                        if prefill_trans and prefill_trans.get("amount"):
                            default_amount = max(0.01, prefill_trans.get("amount", 0.0) / 100)

                        trans_amount = st.number_input(
                            "amount *",
                            min_value=0.01,
                            value=default_amount,
                            step=0.01,
                            format="%.2f",
                            key=f"amount_{idx}"
                        )

                        trans_number = st.text_input(
                            "number *",
                            value=prefill_trans.get("number", "") if prefill_trans else "",
                            key=f"number_{idx}"
                        )

                        default_merchant = "Fake callback - "
                        if prefill_trans and prefill_trans.get("payment_fields"):
                            default_merchant = prefill_trans["payment_fields"].get("merchantName", default_merchant)

                        trans_merchant = st.text_input(
                            "merchantName *",
                            value=default_merchant,
                            key=f"merchant_{idx}"
                        )

                    with col2:
                        # Campos condicionais por tipo
                        if trans_type in ["DEBITO", "CREDITO"]:
                            default_auth = ""
                            if prefill_trans and prefill_trans.get("authorization_code"):
                                default_auth = prefill_trans["authorization_code"]

                            trans_auth = st.text_input(
                                "authorization_code *",
                                value=default_auth,
                                key=f"auth_{idx}"
                            )
                        else:
                            trans_auth = None

                        if trans_type == "CREDITO":
                            # Opções: vazio (0) ou 1-24
                            quotas_options = [""] + [str(i) for i in range(1, 25)]

                            default_quotas_index = 0  # Vazio por padrão
                            if prefill_trans and prefill_trans.get("payment_fields"):
                                quotas_from_prefill = prefill_trans["payment_fields"].get("numberOfQuotas")
                                if quotas_from_prefill and 1 <= quotas_from_prefill <= 24:
                                    default_quotas_index = quotas_from_prefill

                            trans_quotas_str = st.selectbox(
                                "numberOfQuotas *",
                                quotas_options,
                                index=default_quotas_index,
                                key=f"quotas_{idx}",
                                help="Selecione entre 1 e 24 parcelas"
                            )

                            # Converter para inteiro (0 se vazio)
                            trans_quotas = int(trans_quotas_str) if trans_quotas_str else 0
                        else:
                            trans_quotas = None

                    # Preparar dados desta transação
                    trans_data = {
                        "type": trans_type,
                        "amount": trans_amount,
                        "number": trans_number,
                        "merchant_name": trans_merchant
                    }

                    if trans_type in ["DEBITO", "CREDITO"]:
                        trans_data["card_mask"] = "************XXXX"
                        trans_data["card_brand"] = "XXXXXXXX"
                        trans_data["authorization_code"] = trans_auth

                    if trans_type == "CREDITO":
                        trans_data["number_of_quotas"] = int(trans_quotas)

                    # Preservar campos originais se houver pré-preenchimento
                    if prefill_trans:
                        if prefill_trans.get("payment_fields"):
                            trans_data["preserve_payment_fields"] = prefill_trans["payment_fields"]
                        if prefill_trans.get("card"):
                            trans_data["preserve_card"] = prefill_trans["card"]
                        if prefill_trans.get("external_id"):
                            trans_data["preserve_external_id"] = prefill_trans["external_id"]

                    temp_transactions.append(trans_data)

        # Botão para gerar
        if st.button("🚀 Gerar JSON", type="primary"):
            # Validar campos obrigatórios
            all_valid = True
            for i, trans in enumerate(temp_transactions):
                # Se for transação colada (JSON pronto), não validar campos do formulário
                if "type" not in trans:
                    # É um JSON colado pronto - validar apenas número
                    if not trans.get("number"):
                        st.error(f"⚠️ Transação {i+1}: JSON colado precisa ter 'number'!")
                        all_valid = False
                else:
                    # É transação preenchida manualmente - validar campos completos
                    if not trans.get("number") or not trans.get("merchant_name"):
                        st.error(f"⚠️ Transação {i+1}: Preencha todos os campos obrigatórios!")
                        all_valid = False

                    if trans["type"] in ["DEBITO", "CREDITO"]:
                        if not trans.get("authorization_code"):
                            st.error(f"⚠️ Transação {i+1}: Preencha authorization_code!")
                            all_valid = False

                    if trans["type"] == "CREDITO":
                        if not trans.get("number_of_quotas") or trans.get("number_of_quotas") == 0:
                            st.error(f"⚠️ Transação {i+1}: Preencha numberOfQuotas!")
                            all_valid = False

            if all_valid:
                transactions_data = temp_transactions

# PROCESSAR E GERAR JSON
if transactions_data:
    st.markdown("---")
    st.subheader("4️⃣ Resultado")

    try:
        # Parse do cabeçalho
        if not header_json_str.strip():
            st.error("❌ Por favor, cole o JSON do cabeçalho!")
        else:
            # Limpar o JSON: remover vírgula final e adicionar } se necessário
            cleaned_json = header_json_str.strip()

            # Se não termina com }, adicionar
            if not cleaned_json.endswith('}'):
                # Remover vírgula final antes de adicionar }
                if cleaned_json.endswith(','):
                    cleaned_json = cleaned_json.rstrip(',').rstrip()
                cleaned_json += '\n}'

            header_json = json.loads(cleaned_json)

            # Forçar silenciosamente o status do cabeçalho para "PAID"
            header_json["status"] = "PAID"

            # Gerar JSON
            generator = HybrisJSONGenerator()
            result = generator.generate_json_with_header(
                header_json=header_json,
                transaction_type=transaction_type,
                transactions_data=transactions_data
            )

            # Verificar se houve erro
            if isinstance(result, dict) and not result.get("success", True):
                st.error("❌ Erro na validação:")
                for error in result.get("validation_errors", []):
                    st.error(f"  • {error}")
            else:
                # Parse do resultado
                result_obj = json.loads(result)

                # Mostrar sucesso
                st.success("✅ JSON gerado com sucesso!")

                # Informações do resultado
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Número do Pedido", result_obj["number"])
                with col2:
                    st.metric("Total de Transações", len(result_obj["transactions"]))
                with col3:
                    st.metric("Valor Total", f"R$ {result_obj['price']/100:.2f}")

                st.markdown("---")

                # JSON formatado
                st.markdown("### 📄 JSON Gerado:")
                st.code(result, language="json", line_numbers=True)

                # Botão de ação
                st.markdown("### 💾 Ações:")
                # Botão de download
                st.download_button(
                    label="📥 Baixar JSON",
                    data=result,
                    file_name=f"hybris_{result_obj['number']}.json",
                    mime="application/json",
                    use_container_width=True
                )

                # Instruções finais
                st.info("💡 **Próximos passos:** Use o JSON copiado ou baixado no Postman para enviar à API Hybris.")

    except json.JSONDecodeError as e:
        st.error(f"❌ Erro ao fazer parse do JSON do cabeçalho: {str(e)}")
        st.info("💡 Verifique se o JSON colado está no formato correto.")

    except Exception as e:
        st.error(f"❌ Erro ao gerar JSON: {str(e)}")
        st.exception(e)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem 0;">
    <p><strong>Gerador de JSON (Fake Callback) -  Hybris</strong></p>
    <p>Versão 2.0 | Desenvolvido para automação de vinculação de pagamentos</p>
    </div>
""", unsafe_allow_html=True)
