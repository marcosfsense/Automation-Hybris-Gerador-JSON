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
import hashlib                      # Hash para detectar mudanças
from pathlib import Path            # Trabalhar com caminhos de arquivos
from hybris_json_generator import HybrisJSONGenerator  # Classe geradora do JSON

# ═══════════════════════════════════════════════════════════════════════
# AUTENTICAÇÃO - Proteção de acesso
# ═══════════════════════════════════════════════════════════════════════

def load_credentials() -> dict:
    """Carrega credenciais do arquivo JSON"""
    creds_path = Path(__file__).parent.parent / "credentials.json"

    if not creds_path.exists():
        # Credencial padrão se arquivo não existir
        return {
            "users": {
                "marco": {
                    "password_hash": "sha256:a43f1d0aafd193734f329da5c1f88df67aac503afea0320db3825f2396e3e9a8",
                    "enabled": True
                }
            }
        }

    try:
        with open(creds_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        # Retorna padrão em caso de erro
        return {
            "users": {
                "marco": {
                    "password_hash": "sha256:a43f1d0aafd193734f329da5c1f88df67aac503afea0320db3825f2396e3e9a8",
                    "enabled": True
                }
            }
        }

def verify_password(password: str, password_hash: str) -> bool:
    """Verifica se a senha corresponde ao hash SHA256"""
    expected_hash = f"sha256:{hashlib.sha256(password.encode()).hexdigest()}"
    return expected_hash == password_hash

def check_password():
    """Verifica se o usuário está autenticado"""
    def password_entered():
        # Validar credenciais
        username = st.session_state.get("username", "")
        password = st.session_state.get("password", "")

        credentials = load_credentials()
        users = credentials.get("users", {})

        if username in users:
            user = users[username]
            if user.get("enabled", True) and verify_password(password, user.get("password_hash", "")):
                st.session_state["password_correct"] = True
                st.session_state["username_logged"] = username
                del st.session_state["password"]
                del st.session_state["username"]
            else:
                st.session_state["password_correct"] = False
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.set_page_config(page_title="Autenticação", layout="centered")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("# 🔐 Acesso Restrito")
            st.markdown("Autentique-se para continuar")

            username = st.text_input(
                "Usuário:",
                key="username",
            )
            password = st.text_input(
                "Senha:",
                type="password",
                key="password",
                on_change=password_entered
            )
        st.stop()
    elif not st.session_state.get("password_correct", False):
        st.error("❌ Usuário ou senha incorretos!")
        st.stop()

# Verificar autenticação no início
check_password()

# ═══════════════════════════════════════════════════════════════════════
# FUNÇÃO HELPER - Extrair transação de diferentes formatos Hybris
# ═══════════════════════════════════════════════════════════════════════

def validate_header_json(header_data: dict) -> tuple[bool, list]:
    """
    Valida se o JSON do cabeçalho tem os campos obrigatórios.

    Args:
        header_data: Dicionário com dados do cabeçalho

    Returns:
        (is_valid: bool, errors: list of strings)
    """
    errors = []

    if not header_data:
        return False, ["Header vazio ou não carregado"]

    # Campos obrigatórios do cabeçalho
    if not header_data.get("id"):
        errors.append("'id' é obrigatório no cabeçalho")

    if not header_data.get("price") and header_data.get("price") != 0:
        errors.append("'price' é obrigatório no cabeçalho")

    if not header_data.get("number"):
        errors.append("'number' é obrigatório no cabeçalho")

    if not header_data.get("items") or not isinstance(header_data["items"], list):
        errors.append("'items' é obrigatório no cabeçalho (deve ser um array)")

    if not header_data.get("created_at"):
        errors.append("'created_at' é obrigatório no cabeçalho")

    if not header_data.get("updated_at"):
        errors.append("'updated_at' é obrigatório no cabeçalho")

    return len(errors) == 0, errors


def validate_json_transaction(trans_data: dict, trans_type: str = None) -> tuple[bool, list]:
    """
    Valida se o JSON colado tem os campos obrigatórios.

    Args:
        trans_data: Dicionário com dados da transação
        trans_type: Tipo esperado (PIX, DEBITO, CREDITO) ou None para auto-detectar

    Returns:
        (is_valid: bool, errors: list of strings)
    """
    errors = []

    if not trans_data:
        return False, ["JSON vazio ou não carregado"]

    # Campos universalmente obrigatórios
    if not trans_data.get("amount") and trans_data.get("amount") != 0:
        errors.append("'amount' é obrigatório")

    if not trans_data.get("number"):
        errors.append("'number' é obrigatório")

    # Detectar tipo se não informado
    if not trans_type:
        if "payment_fields" in trans_data:
            product_code = trans_data["payment_fields"].get("primaryProductCode")
            if product_code == 25:
                trans_type = "PIX"
            elif product_code == 2000:
                trans_type = "DEBITO"
            elif product_code == 1000:
                trans_type = "CREDITO"

    # Validação por tipo
    if trans_type == "PIX":
        if not trans_data.get("payment_fields"):
            errors.append("'payment_fields' é obrigatório para PIX")
        elif not trans_data["payment_fields"].get("merchantName"):
            errors.append("'payment_fields.merchantName' é obrigatório para PIX")

    elif trans_type == "DEBITO":
        if not trans_data.get("card"):
            errors.append("'card' é obrigatório para DÉBITO")
        elif not trans_data["card"].get("mask") or not trans_data["card"].get("brand"):
            errors.append("'card.mask' e 'card.brand' são obrigatórios para DÉBITO")

        if not trans_data.get("authorization_code"):
            errors.append("'authorization_code' é obrigatório para DÉBITO")

        if not trans_data.get("payment_fields"):
            errors.append("'payment_fields' é obrigatório para DÉBITO")
        elif not trans_data["payment_fields"].get("merchantName"):
            errors.append("'payment_fields.merchantName' é obrigatório para DÉBITO")

    elif trans_type == "CREDITO":
        if not trans_data.get("card"):
            errors.append("'card' é obrigatório para CRÉDITO")
        elif not trans_data["card"].get("mask") or not trans_data["card"].get("brand"):
            errors.append("'card.mask' e 'card.brand' são obrigatórios para CRÉDITO")

        if not trans_data.get("authorization_code"):
            errors.append("'authorization_code' é obrigatório para CRÉDITO")

        if not trans_data.get("payment_fields"):
            errors.append("'payment_fields' é obrigatório para CRÉDITO")
        elif not trans_data["payment_fields"].get("merchantName"):
            errors.append("'payment_fields.merchantName' é obrigatório para CRÉDITO")
        # numberOfQuotas pode ser 0 em JSONs colados, então apenas verificar se existe a chave
        elif "numberOfQuotas" not in trans_data["payment_fields"]:
            errors.append("'payment_fields.numberOfQuotas' é obrigatório para CRÉDITO")

    return len(errors) == 0, errors


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


def try_fix_incomplete_json(json_str: str) -> str:
    """
    Tenta corrigir JSONs incompletos ou mal formados.

    Estratégias:
    1. Remove símbolos extras no final (] } etc)
    2. Se não começa com {, adiciona
    3. Se não termina com }, adiciona
    4. Remove vírgula final antes de adicionar }
    5. Tenta várias combinações de chaves de fechamento

    Args:
        json_str: String JSON potencialmente incompleta ou mal formada

    Returns:
        String JSON corrigida (ou original se não conseguir)
    """
    json_str = json_str.strip()

    # Se JSON está vazio, retorna
    if not json_str:
        return json_str

    # Estratégia PRÉ-0: Corrigir estrutura básica (adicionar { se falta)
    original_json_str = json_str

    # Primeiro: adicionar { no início se não houver
    if not json_str.startswith('{'):
        json_str = '{\n' + json_str

    # Segundo: encontrar a posição do primeiro } que fecha o objeto raiz
    # e remover tudo após ele
    brace_count = 0
    last_valid_brace_pos = -1

    for i, char in enumerate(json_str):
        if char == '{':
            brace_count += 1
        elif char == '}':
            brace_count -= 1
            if brace_count == 0:
                # Encontrou o fechamento do objeto raiz
                last_valid_brace_pos = i + 1
                break

    if last_valid_brace_pos > 0:
        json_str = json_str[:last_valid_brace_pos]

    # Se agora está vazio, retorna original
    if not json_str:
        return original_json_str

    # Se já está bem formado, retorna
    if json_str.startswith('{') and json_str.endswith('}'):
        try:
            json.loads(json_str)
            return json_str
        except json.JSONDecodeError:
            pass

    # Estratégia 1: Adicionar } no final
    if not json_str.endswith('}'):
        if json_str.endswith(','):
            # Remove vírgula e adiciona }
            fixed = json_str.rstrip(',').rstrip() + '\n}'
        else:
            # Adiciona direto
            fixed = json_str + '\n}'

        # Tentar fazer parse para validar
        try:
            json.loads(fixed)
            return fixed
        except json.JSONDecodeError:
            pass

    # Estratégia 2: Tentar adicionar múltiplos } (para JSONs mais complexos)
    for num_braces in range(2, 6):
        fixed = json_str.rstrip(',').rstrip()
        if not fixed.startswith('{'):
            fixed = '{\n' + fixed
        fixed = fixed + '\n' + ('}' * num_braces)
        try:
            json.loads(fixed)
            return fixed
        except json.JSONDecodeError:
            pass

    # Se nenhuma estratégia funcionou, retorna original
    return original_json_str


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
# FORÇA TEMA ESCURO - Configuração direta em JavaScript
# ═══════════════════════════════════════════════════════════════════════

# Injetar JavaScript para forçar tema escuro (caso config.toml não funcione)
st.markdown("""
<script>
    // Força tema escuro no Streamlit
    let darkModeToggle = document.querySelector('[data-testid="stAppViewContainer"]');
    if (darkModeToggle) {
        // Tenta mudar tema para dark
        document.documentElement.setAttribute('data-theme', 'dark');
    }
</script>
""", unsafe_allow_html=True)

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

# Inicializar session_state para o header se não existir
if "header_json_input" not in st.session_state:
    st.session_state.header_json_input = ""

header_json_str = st.text_area(
    "Cole aqui o JSON do cabeçalho do pedido (até antes de 'transactions'):",
    value=st.session_state.header_json_input,
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
    help="Cole até antes de 'transactions'. Pode ter vírgula no final - o sistema corrige.",
    key="header_json_input"
)

st.markdown("---")

# SEÇÃO 2: TIPO DE TRANSAÇÃO
st.subheader("2️⃣ Tipo de Transação")

transaction_type = st.selectbox(
    "Selecione o tipo de transação:",
    ["", "PIX", "DEBITO", "CREDITO", "MULTIPLAS"],
    help="Escolha o tipo de pagamento que será vinculado",
    key="transaction_type_select"
)

# Se mudou o tipo de transação, resetar flag de JSON gerado
if 'previous_transaction_type' not in st.session_state:
    st.session_state.previous_transaction_type = transaction_type
elif st.session_state.previous_transaction_type != transaction_type:
    st.session_state.json_generated = False
    st.session_state.generated_result = None
    st.session_state.generated_result_obj = None
    st.session_state.previous_transaction_type = transaction_type

st.markdown("---")

# SEÇÃO 2.5: NOME DO ESTABELECIMENTO (MERCHANT) - OBRIGATÓRIO
st.subheader("2️⃣.5️⃣ Nome do Estabelecimento (Obrigatório)")

st.info("ℹ️ **Importante:** Este campo será usado em TODAS as transações. Personalize com o nome da pessoa e assunto do email de solicitação.")

# Inicializar session_state para merchant_name global se não existir
if "global_merchant_name" not in st.session_state:
    st.session_state.global_merchant_name = "Fake callback - "

global_merchant_name = st.text_input(
    "Nome do Estabelecimento *",
    value=st.session_state.global_merchant_name,
    placeholder="Ex: Fake callback - João Silva - RE: Transferência de 15/11/2024",
    help="Personalize este campo com o nome da pessoa e o assunto da operação",
    key="global_merchant_name"
)

st.markdown("---")

# Inicializar variáveis
transactions_data = []
result_json = None
error_message = None
prefill_data = None  # Inicializar prefill_data (removida seção 2.1)

# Inicializar session_state para controlar regeneração
if 'json_generated' not in st.session_state:
    st.session_state.json_generated = False
if 'generated_result' not in st.session_state:
    st.session_state.generated_result = None
if 'generated_result_obj' not in st.session_state:
    st.session_state.generated_result_obj = None
if 'last_header_json_hash' not in st.session_state:
    st.session_state.last_header_json_hash = None

# Detectar mudanças no header JSON para resetar json_generated
current_header_hash = hashlib.md5(header_json_str.encode()).hexdigest()
if st.session_state.last_header_json_hash != current_header_hash:
    st.session_state.json_generated = False
    st.session_state.generated_result = None
    st.session_state.generated_result_obj = None
    st.session_state.last_header_json_hash = current_header_hash

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
                    # Tentar corrigir JSON incompleto
                    cleaned_pix_json = try_fix_incomplete_json(pix_json_str.strip())
                    json_loaded = json.loads(cleaned_pix_json)
                    # Extrair transação de diferentes formatos Hybris
                    prefill_pix_json = extract_transaction_from_hybris(json_loaded)
                    # Normalizar amount: converter centavos para Reais se necessário
                    if prefill_pix_json and "amount" in prefill_pix_json:
                        prefill_pix_json["amount"] = normalize_amount_from_json(prefill_pix_json["amount"])

                    # Validar se tem campos obrigatórios
                    is_valid, errors = validate_json_transaction(prefill_pix_json, "PIX")
                    if not is_valid:
                        st.warning("⚠️ JSON tem problemas:")
                        for error in errors:
                            st.warning(f"  • {error}")
                        prefill_pix_json = None
                    else:
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
                    min_value=0.00,
                    value=prefill_pix.get("amount", 0.0) / 100 if prefill_pix else 0.00,
                    step=0.01,
                    format="%.2f",
                    help="Valor da transação em Reais",
                    key="pix_amount_input"
                )

                pix_number = st.text_input(
                    "number *",
                    value=prefill_pix.get("number", "") if prefill_pix else "",
                    help="Número da transação/terminal"
                )

            with col2:
                # Usar merchant_name global (preenchido na seção 2.5)
                pix_merchant_name = st.text_input(
                    "merchantName *",
                    value=global_merchant_name,
                    help="Nome do estabelecimento comercial (preenchido na seção acima)",
                    disabled=True  # Desabilitar pois o valor vem da seção 2.5
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

            # Botão para gerar
            if st.button("🚀 Gerar JSON", type="primary"):
                # Formulário manual - validar campos
                if not pix_number or not pix_merchant_name:
                    st.error("⚠️ Por favor, preencha todos os campos obrigatórios!")
                else:
                    transactions_data = [trans_data]

        # Bloco para JSON colado
        if pix_has_existing == "Sim":
            # Botão para gerar (quando JSON colado)
            if st.button("🚀 Gerar JSON", type="primary", key="pix_gerar_json"):
                # JSON colado - validar apenas número
                if not transactions_data or not transactions_data[0].get("number"):
                    st.error("⚠️ JSON colado precisa ter 'number'!")
                else:
                    transactions_data = [transactions_data[0]]

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
                    # Tentar corrigir JSON incompleto
                    cleaned_deb_json = try_fix_incomplete_json(deb_json_str.strip())
                    json_loaded = json.loads(cleaned_deb_json)
                    # Extrair transação de diferentes formatos Hybris
                    prefill_deb_json = extract_transaction_from_hybris(json_loaded)
                    # Normalizar amount: converter centavos para Reais se necessário
                    if prefill_deb_json and "amount" in prefill_deb_json:
                        prefill_deb_json["amount"] = normalize_amount_from_json(prefill_deb_json["amount"])

                    # Validar se tem campos obrigatórios
                    is_valid, errors = validate_json_transaction(prefill_deb_json, "DEBITO")
                    if not is_valid:
                        st.warning("⚠️ JSON tem problemas:")
                        for error in errors:
                            st.warning(f"  • {error}")
                        prefill_deb_json = None
                    else:
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
                    min_value=0.00,
                    value=prefill_deb.get("amount", 0.0) / 100 if prefill_deb else 0.00,
                    step=0.01,
                    format="%.2f",
                    key="deb_amount_input"
                )

                deb_number = st.text_input(
                    "number *",
                    value=prefill_deb.get("number", "") if prefill_deb else ""
                )

            with col2:
                # Usar merchant_name global (preenchido na seção 2.5)
                deb_merchant_name = st.text_input(
                    "merchantName *",
                    value=global_merchant_name,
                    help="Nome do estabelecimento comercial (preenchido na seção acima)",
                    disabled=True  # Desabilitar pois o valor vem da seção 2.5
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

            # Botão para gerar
            if st.button("🚀 Gerar JSON", type="primary"):
                # Formulário manual - validar campos
                if not all([deb_number, deb_merchant_name, deb_auth_code]):
                    st.error("⚠️ Por favor, preencha todos os campos obrigatórios!")
                else:
                    transactions_data = [trans_data]

        # Bloco para JSON colado
        if deb_has_existing == "Sim":
            # Botão para gerar (quando JSON colado)
            if st.button("🚀 Gerar JSON", type="primary", key="deb_gerar_json"):
                # JSON colado - validar apenas número
                if not transactions_data or not transactions_data[0].get("number"):
                    st.error("⚠️ JSON colado precisa ter 'number'!")
                else:
                    transactions_data = [transactions_data[0]]

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
                    # Tentar corrigir JSON incompleto
                    cleaned_cred_json = try_fix_incomplete_json(cred_json_str.strip())
                    json_loaded = json.loads(cleaned_cred_json)
                    # Extrair transação de diferentes formatos Hybris
                    prefill_cred_json = extract_transaction_from_hybris(json_loaded)
                    # Normalizar amount: converter centavos para Reais se necessário
                    if prefill_cred_json and "amount" in prefill_cred_json:
                        prefill_cred_json["amount"] = normalize_amount_from_json(prefill_cred_json["amount"])

                    # Validar se tem campos obrigatórios
                    is_valid, errors = validate_json_transaction(prefill_cred_json, "CREDITO")
                    if not is_valid:
                        st.warning("⚠️ JSON tem problemas:")
                        for error in errors:
                            st.warning(f"  • {error}")
                        prefill_cred_json = None
                    else:
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
                    min_value=0.00,
                    value=prefill_cred.get("amount", 0.0) / 100 if prefill_cred else 0.00,
                    step=0.01,
                    format="%.2f",
                    key="cred_amount_input"
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
                # Usar merchant_name global (preenchido na seção 2.5)
                cred_merchant_name = st.text_input(
                    "merchantName *",
                    value=global_merchant_name,
                    help="Nome do estabelecimento comercial (preenchido na seção acima)",
                    disabled=True  # Desabilitar pois o valor vem da seção 2.5
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

            # Botão para gerar
            if st.button("🚀 Gerar JSON", type="primary"):
                # Formulário manual - validar campos
                if not all([cred_number, cred_merchant_name, cred_auth_code]) or cred_quotas == 0:
                    st.error("⚠️ Por favor, preencha todos os campos obrigatórios (incluindo numberOfQuotas)!")
                else:
                    transactions_data = [trans_data]

        # Bloco para JSON colado
        if cred_has_existing == "Sim":
            # Botão para gerar (quando JSON colado)
            if st.button("🚀 Gerar JSON", type="primary", key="cred_gerar_json"):
                # JSON colado - validar apenas número
                if not transactions_data or not transactions_data[0].get("number"):
                    st.error("⚠️ JSON colado precisa ter 'number'!")
                else:
                    transactions_data = [transactions_data[0]]

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

        # Reinicializar temp_transactions a cada render (importante para Streamlit)
        temp_transactions = [None] * int(num_transactions)

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
                            # Tentar corrigir JSON incompleto
                            fixed_json_str = try_fix_incomplete_json(existing_trans_str.strip())
                            json_loaded = json.loads(fixed_json_str)
                            # Extrair transação de diferentes formatos Hybris
                            prefill_trans = extract_transaction_from_hybris(json_loaded)
                            # Normalizar amount: converter centavos para Reais se necessário
                            if prefill_trans and "amount" in prefill_trans:
                                prefill_trans["amount"] = normalize_amount_from_json(prefill_trans["amount"])

                            # Validar se tem campos obrigatórios (auto-detectar tipo)
                            is_valid, errors = validate_json_transaction(prefill_trans)

                            # Mostrar validação com st.divider para ser mais visível
                            st.divider()
                            if not is_valid:
                                st.warning(f"⚠️ Transação {idx+1} tem problemas:")
                                for error in errors:
                                    st.warning(f"  • {error}")
                                prefill_trans = None
                            else:
                                st.success(f"✅ Transação {idx+1} carregada com sucesso!")
                        except json.JSONDecodeError as e:
                            st.divider()
                            st.error(f"❌ Erro ao fazer parse do JSON: {str(e)}")
                            prefill_trans = None

                    # Apenas preparar dados do JSON colado
                    trans_data = prefill_trans if prefill_trans else {}
                    if trans_data:
                        temp_transactions[idx] = trans_data

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
                        default_amount = 0.00
                        if prefill_trans and prefill_trans.get("amount"):
                            default_amount = max(0.00, prefill_trans.get("amount", 0.0) / 100)

                        trans_amount = st.number_input(
                            "amount *",
                            min_value=0.00,
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

                        # Usar merchant_name global (preenchido na seção 2.5)
                        trans_merchant = st.text_input(
                            "merchantName *",
                            value=global_merchant_name,
                            key=f"merchant_{idx}",
                            help="Nome do estabelecimento comercial (preenchido na seção 2.5)",
                            disabled=True  # Desabilitar pois o valor vem da seção 2.5
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

                    temp_transactions[idx] = trans_data

        # Botão para gerar
        if st.button("🚀 Gerar JSON", type="primary"):
            # Filtrar transações válidas (remover None)
            valid_transactions = [t for t in temp_transactions if t is not None]

            # Validar se tem pelo menos 2 transações
            if len(valid_transactions) < 2:
                st.error(f"⚠️ Preencha pelo menos 2 transações! Você preencheu {len(valid_transactions)}.")
            else:
                # Validar campos obrigatórios
                all_valid = True
                for i, trans in enumerate(valid_transactions):
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
                    transactions_data = valid_transactions

# GERAR JSON (quando há dados a consolidar)
# Esta seção processa e gera o JSON, armazenando em session_state
if transactions_data and not st.session_state.json_generated:
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

            # Validar se o header tem campos obrigatórios
            is_valid, errors = validate_header_json(header_json)
            if not is_valid:
                st.error("❌ Cabeçalho tem problemas:")
                for error in errors:
                    st.error(f"  • {error}")
            else:
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
                    # Armazenar resultado em session_state
                    result_obj = json.loads(result)
                    st.session_state.generated_result = result
                    st.session_state.generated_result_obj = result_obj
                    st.session_state.json_generated = True
                    st.rerun()  # Reexecuta a página para mostrar resultado

    except json.JSONDecodeError as e:
        st.error(f"❌ Erro ao fazer parse do JSON do cabeçalho: {str(e)}")
        st.info("💡 **Dicas para corrigir o erro:**")
        st.info("• Verifique se há vírgula dupla ou dados duplicados")
        st.info("• Remova qualquer texto após o JSON")
        st.info("• Certifique-se de que não há caracteres extras no final")
        st.info("• Se houver múltiplos JSONs colados, separe um de cada vez")
    except Exception as e:
        st.error(f"❌ Erro ao gerar JSON: {str(e)}")
        st.exception(e)

# MOSTRAR RESULTADO ARMAZENADO
# Mostrar resultado apenas se JSON já foi gerado (evita regeneração ao editar transações)
if st.session_state.json_generated and st.session_state.generated_result:
    st.markdown("---")
    st.subheader("4️⃣ Resultado (Consolidado)")

    # Usar resultado armazenado em session_state (não regenerar)
    result = st.session_state.generated_result
    result_obj = st.session_state.generated_result_obj

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

    # COMPARAÇÃO DE TOTAIS: Header vs Transações
    st.markdown("### 💰 Validação de Totais:")

    header_total = result_obj["price"]  # em centavos

    # Calcular soma das transações
    transactions_total = 0
    for trans in result_obj["transactions"]:
        transactions_total += trans.get("amount", 0)

    # Formatar para exibição
    header_total_reais = header_total / 100
    transactions_total_reais = transactions_total / 100
    difference = abs(header_total - transactions_total)
    difference_reais = difference / 100

    # Cores baseadas em match/discrepância
    if header_total == transactions_total:
        status = "✅ MATCH"
        status_color = "green"
        message = "Totais conferem perfeitamente!"
    elif difference <= 100:  # até R$ 1 de diferença
        status = "⚠️ AVISO"
        status_color = "orange"
        message = f"Pequena diferença de R$ {difference_reais:.2f}"
    else:
        status = "❌ ERRO"
        status_color = "red"
        message = f"Diferença de R$ {difference_reais:.2f}"

    # Exibir cards de comparação
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        <div style="
            background-color: #f0f2f6;
            padding: 20px;
            border-radius: 10px;
            border-left: 5px solid #3498db;
        ">
            <h4 style="margin-top: 0; color: #333;">📋 Total do Cabeçalho</h4>
            <p style="font-size: 24px; font-weight: bold; color: #3498db; margin: 10px 0;">
                R$ {header_total_reais:,.2f}
            </p>
            <p style="color: #666; font-size: 12px; margin: 0;">
                Valor total do pedido (price)
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style="
            background-color: #f0f2f6;
            padding: 20px;
            border-radius: 10px;
            border-left: 5px solid #27ae60;
        ">
            <h4 style="margin-top: 0; color: #333;">💳 Soma das Transações</h4>
            <p style="font-size: 24px; font-weight: bold; color: #27ae60; margin: 10px 0;">
                R$ {transactions_total_reais:,.2f}
            </p>
            <p style="color: #666; font-size: 12px; margin: 0;">
                Soma de all amounts
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Status de validação
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"**Status:** {message}")
    with col2:
        if status_color == "green":
            st.success(status)
        elif status_color == "orange":
            st.warning(status)
        else:
            st.error(status)

    st.markdown("---")

    # JSON formatado
    st.markdown("### 📄 JSON Gerado:")
    st.code(result, language="json", line_numbers=True)

    # Botão de ação
    st.markdown("### 💾 Ações:")

    col1, col2 = st.columns(2)

    with col1:
        # Botão de download
        st.download_button(
            label="📥 Baixar JSON",
            data=result,
            file_name=f"hybris_{result_obj['number']}.json",
            mime="application/json",
            use_container_width=True
        )

    with col2:
        # Botão Clear All
        if st.button("🔄 Limpar Tudo", use_container_width=True):
            # Resetar TODOS os session states
            st.session_state.json_generated = False
            st.session_state.generated_result = None
            st.session_state.generated_result_obj = None
            st.session_state.previous_transaction_type = ""
            st.session_state.last_header_json_hash = None

            # Limpar também o selectbox de tipo de transação
            if "transaction_type_select" in st.session_state:
                del st.session_state.transaction_type_select

            # Limpar também o text_area do header JSON
            if "header_json_input" in st.session_state:
                del st.session_state.header_json_input

            # Limpar também o merchant_name global
            if "global_merchant_name" in st.session_state:
                st.session_state.global_merchant_name = "Fake callback - "

            # Reexecutar página para mostrar formulário vazio
            st.rerun()

    # Instruções finais
    st.info("💡 **Próximos passos:** Use o JSON copiado ou baixado no Postman para enviar à API Hybris.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem 0;">
    <p><strong>Gerador de JSON (Fake Callback) -  Hybris</strong></p>
    <p>Versão 2.0 | Desenvolvido para automação de vinculação de pagamentos</p>
    </div>
""", unsafe_allow_html=True)
