# ═══════════════════════════════════════════════════════════════════════════════
# GERADOR DE JSONs PARA HYBRIS - VERSÃO COM COMENTÁRIOS COMPLETOS
# ═══════════════════════════════════════════════════════════════════════════════

# IMPORTS - Importações necessárias para o funcionamento do código
from datetime import datetime        # Para trabalhar com datas e horas
import json                         # Para manipular JSON (parse, dumps, loads)
from typing import Dict, List, Optional  # Type hints (Dict, List, Optional)
import random                       # Para gerar números/caracteres aleatórios
import string                       # Constantes: ascii_lowercase, digits, etc
from zoneinfo import ZoneInfo       # Timezone com DST automático (Python 3.9+)


# ═══════════════════════════════════════════════════════════════════════════════
# CLASSE PRINCIPAL - HybrisJSONGenerator
# ═══════════════════════════════════════════════════════════════════════════════

class HybrisJSONGenerator:
    """Classe principal para gerar JSONs de transações para o sistema Hybris

    Características principais:
    - Gera IDs únicos de 42 caracteres (a-z, 0-9)
    - Suporta PIX, DÉBITO, CRÉDITO e MÚLTIPLAS transações
    - Validação automática de cabeçalho e campos obrigatórios
    - Timestamps em timezone de São Paulo (Brasil) com DST
    - Preservação de campos originais do JSON colado
    - Conversão automática entre Reais e centavos
    """

    def __init__(self):
        """Inicializa o gerador com timezone de São Paulo

        O timezone ajusta automaticamente para horário de verão (DST)
        Exemplo de timestamp gerado: "2024-11-13T15:30:45.123456-03:00"
        """
        # Timezone de São Paulo que ajusta automaticamente DST
        self.brazil_tz = ZoneInfo("America/Sao_Paulo")

        # Timestamp atual em ISO 8601 com timezone
        self.current_timestamp = datetime.now(self.brazil_tz).isoformat()

    # ═══════════════════════════════════════════════════════════════════════════
    # MÉTODOS ESTÁTICOS - Funções auxiliares que não precisam de self
    # ═══════════════════════════════════════════════════════════════════════════

    @staticmethod
    def generate_unique_id() -> str:
        """Gera um ID único de 42 caracteres alfanuméricos (sem traços)

        Formato: apenas letras minúsculas (a-z) e números (0-9)
        Comprimento: exatamente 42 caracteres
        Exemplo: 4216b627fb0841ce8e5eb44eeda9b3b4aa26624a13d

        Returns:
            str: ID único de 42 caracteres
        """
        # Define conjunto de caracteres permitidos (a-z e 0-9)
        chars = string.ascii_lowercase + string.digits
        # Exemplos de chars: "abcdefghijklmnopqrstuvwxyz0123456789"

        # Gera 42 caracteres aleatórios
        unique_id = ''.join(random.choice(chars) for _ in range(42))
        # random.choice(chars) = seleciona aleatoriamente um caractere
        # for _ in range(42) = repete 42 vezes
        # ''.join(...) = junta todos em uma string

        return unique_id

    @staticmethod
    def format_money(value: float) -> int:
        """Converte valor em reais para centavos (inteiro)

        O Hybris trabalha com valores em centavos para evitar
        problemas de precisão com números decimais.

        Args:
            value (float): Valor em reais (ex: 100.50)

        Returns:
            int: Valor em centavos (ex: 10050)

        Exemplos:
            format_money(100.50) → 10050
            format_money(5990.00) → 599000
            format_money(1.99) → 199
        """
        return int(value * 100)

    @staticmethod
    def parse_money(cents: int) -> float:
        """Converte centavos para reais

        Função inversa de format_money(). Reconverte centavos
        para o formato de reais para exibição.

        Args:
            cents (int): Valor em centavos (ex: 10050)

        Returns:
            float: Valor em reais (ex: 100.50)

        Exemplos:
            parse_money(10050) → 100.50
            parse_money(599000) → 5990.00
            parse_money(199) → 1.99
        """
        return cents / 100

    # ═══════════════════════════════════════════════════════════════════════════
    # VALIDAÇÃO - Métodos para validar dados de entrada
    # ═══════════════════════════════════════════════════════════════════════════

    def validate_header_json(self, header_json: Dict) -> tuple[bool, List[str]]:
        """Valida se o JSON do cabeçalho possui todos os campos obrigatórios

        Este método verifica se o JSON copiado do Hybris está completo
        e correto antes de processar as transações.

        Args:
            header_json (Dict): Dicionário com dados do cabeçalho

        Returns:
            tuple[bool, List[str]]: (é_válido, lista_de_erros)
                - é_válido: True se sem erros, False se tiver erros
                - lista_de_erros: Lista com mensagens de erro (vazia se válido)

        Exemplos:
            is_valid, errors = generator.validate_header_json(header)
            if is_valid:
                print("JSON válido")
            else:
                for error in errors:
                    print(f"Erro: {error}")
        """
        errors = []  # Lista para armazenar erros encontrados

        # Lista de campos que DEVEM estar presentes na raiz do JSON
        required_fields = [
            "id",           # ID único do pedido (UUID)
            "items",        # Array com itens do pedido
            "price",        # Valor total em centavos
            "number",       # Número do pedido
            "status",       # Status (deve ser "PAID")
            "reference",    # Referência do pedido
            "created_at",   # Data de criação (ISO 8601)
            "updated_at"    # Data de atualização (ISO 8601)
        ]

        # Verificar se cada campo obrigatório existe
        for field in required_fields:
            if field not in header_json:
                errors.append(f"Campo obrigatório ausente no cabeçalho: '{field}'")

        # Validações específicas para o campo "items"
        if "items" in header_json:
            # Verifica se items é uma lista (array)
            if not isinstance(header_json["items"], list):
                errors.append("Campo 'items' deve ser um array")

            # Verifica se a lista de items não está vazia
            elif len(header_json["items"]) == 0:
                errors.append("Campo 'items' não pode estar vazio")

            else:
                # Validar campos obrigatórios do primeiro item
                item_required = [
                    "id",           # ID do item
                    "sku",          # Código de produto
                    "name",         # Nome do item
                    "uuid",         # UUID único
                    "quantity",     # Quantidade
                    "created_at",   # Data criação
                    "unit_price",   # Preço unitário
                    "updated_at"    # Data atualização
                ]

                # Pega o primeiro item da lista
                item = header_json["items"][0]

                # Verifica cada campo obrigatório do item
                for field in item_required:
                    if field not in item:
                        errors.append(f"Campo obrigatório ausente em items[0]: '{field}'")

        # Validações específicas para o campo "price"
        if "price" in header_json:
            # Verifica se price é numérico (int ou float)
            if not isinstance(header_json["price"], (int, float)):
                errors.append("Campo 'price' deve ser numérico")

            # Verifica se price é maior que zero
            elif header_json["price"] <= 0:
                errors.append("Campo 'price' deve ser maior que zero")

        # Validações específicas para o campo "status"
        if "status" in header_json and header_json["status"] != "PAID":
            errors.append("Campo 'status' deve ser 'PAID'")

        # Determina se JSON é válido (sem erros)
        is_valid = len(errors) == 0

        # Retorna tupla com resultado e lista de erros
        return is_valid, errors

    # ═══════════════════════════════════════════════════════════════════════════
    # CRIAÇÃO DE TRANSAÇÕES - Métodos para gerar cada tipo de transação
    # ═══════════════════════════════════════════════════════════════════════════

    def create_pix_transaction(
        self,
        amount: int,                              # Valor em centavos
        merchant_name: str,                       # Nome do comerciante
        merchant_code: str = "0027822336749400",  # Código do comerciante (padrão)
        terminal_number: str = "11111111",        # Número terminal (padrão)
        authorization_code: Optional[str] = None, # Código de autorização (opcional)
        created_at: Optional[str] = None,         # Timestamp customizado (opcional)
        preserve_payment_fields: Optional[Dict] = None  # Preservar campos originais
    ) -> Dict:
        """Cria uma transação PIX

        PIX é um pagamento instantâneo, portanto não requer cartão
        ou códigos de autorização complexos.

        Args:
            amount (int): Valor em centavos (ex: 10050 = R$ 100.50)
            merchant_name (str): Nome do comerciante (ex: "Loja XYZ")
            merchant_code (str): Código do comerciante (padrão: "0027822336749400")
            terminal_number (str): Número do terminal (padrão: "11111111")
            authorization_code (str, optional): Código de autorização
            created_at (str, optional): Timestamp customizado
            preserve_payment_fields (Dict, optional): Campos originais para preservar

        Returns:
            Dict: Dicionário com dados completos da transação PIX

        Código do Produto PIX:
            primaryProductCode = 25  # PIX é sempre código 25
        """

        # Gera ID único para a transação (42 caracteres)
        transaction_id = self.generate_unique_id()

        # Define timestamp (usa customizado ou timestamp atual)
        timestamp = created_at or self.current_timestamp

        # Define código de autorização (usa fornecido ou gera novo)
        auth_code = authorization_code or self.generate_unique_id()

        # Campos padrão para transação PIX
        default_payment_fields = {
            "v40Code": 0,                    # Código interno Hybris
            "cityState": "Fake callback",    # Cidade (padrão)
            "clientName": "Fake callback",   # Nome cliente (padrão)
            "statusCode": 0,                 # Status padrão
            "hasPassword": False,            # PIX não requer senha
            "hasWarranty": False,            # Sem garantia
            "productName": "PIX PAGAMENTO",  # Nome do produto
            "requestDate": int(datetime.now().strftime("%y%m%d%H%M%S")),
            "documentType": "J",             # J = Pessoa Jurídica
            "hasSignature": False,           # Sem assinatura
            "merchantCode": merchant_code,   # Código comerciante
            "merchantName": merchant_name,   # Nome comerciante
            "applicationId": "cielo.launcher",  # ID da aplicação
            "totalizerCode": 0,              # Código totalizador
            "isExternalCall": True,          # Chamada externa
            "numberOfQuotas": 0,             # PIX não tem parcelas
            "applicationName": "cielo.launcher.ORDER",
            "cardCaptureType": 0,            # Tipo de captura do cartão
            "hasConnectivity": False,        # Sem conectividade
            "merchantAddress": "RUA EXEMPLO",  # Endereço (padrão)
            "paymentTypeCode": 0,            # Código tipo pagamento
            "hasSentReference": False,       # Não enviou referência
            "isFinancialProduct": True,      # É produto financeiro
            "primaryProductCode": 25,        # PIX = código 25
            "primaryProductName": "PIX",     # Nome do produto
            "hasSentMerchantCode": False,    # Não enviou código comerciante
            "paymentTransactionId": self.generate_unique_id(),  # ID único transação
            "secondaryProductCode": 1,       # Código secundário
            "secondaryProductName": "PAGAMENTO",  # Nome secundário
            "receiptPrintPermission": 0,     # Permissão recibo
            "hasPrintedClientReceipt": False,  # Recibo não impresso
            "isDoubleFontPrintAllowed": False,  # Sem fonte dupla
            "isOnlyIntegrationCancelable": False  # Não só integrável
        }

        # Se fornecido, preserva campos originais do JSON colado
        if preserve_payment_fields:
            # Copia campos originais
            payment_fields = {**preserve_payment_fields}
            # Atualiza com novo merchant name (permite customização)
            payment_fields["merchantName"] = merchant_name
            payment_fields["merchantCode"] = merchant_code
            # Preserva paymentTransactionId original (não gera novo)
        else:
            # Usa campos padrão
            payment_fields = default_payment_fields

        # Retorna dicionário com transação completa
        return {
            "id": transaction_id,                # ID único da transação
            "uuid": transaction_id,              # UUID (mesmo que id)
            "amount": amount,                    # Valor em centavos
            "number": terminal_number,           # Número do terminal
            "status": "CONFIRMED",               # Status confirmado
            "created_at": timestamp,             # Data criação
            "updated_at": timestamp,             # Data atualização
            "description": "",                   # Descrição vazia para PIX
            "payment_fields": payment_fields,    # Campos específicos PIX
            "terminal_number": terminal_number,  # Número do terminal
            "transaction_type": "PAYMENT",       # Tipo transação
            "authorization_code": auth_code      # Código autorização
        }

    # ═══════════════════════════════════════════════════════════════════════════
    # ... create_debit_transaction() e create_credit_transaction() seguem padrão similar
    # ═══════════════════════════════════════════════════════════════════════════

    def validate_transaction_totals(self, header_price: int, transactions: List[Dict]) -> bool:
        """Valida se a soma das transações bate com o valor total do cabeçalho

        Este é um verificação importante: a soma dos valores de todas
        as transações DEVE ser igual ao price do cabeçalho.

        Args:
            header_price (int): Valor total em centavos do cabeçalho
            transactions (List[Dict]): Lista com todas as transações

        Returns:
            bool: True se valores batem, False se não batem

        Exemplo:
            header_price = 100000  # R$ 1000.00
            transactions = [
                {"amount": 60000},  # R$ 600.00
                {"amount": 40000}   # R$ 400.00
            ]
            # Soma = 60000 + 40000 = 100000 ✓ OK
        """
        # Calcula soma de todos os amounts das transações
        transactions_total = sum(t["amount"] for t in transactions)

        # Verifica se suma bate com header
        if header_price != transactions_total:
            # Se não bater, imprime aviso (mas não falha)
            print(f"⚠️ AVISO: Soma das transações ({transactions_total}) "
                  f"difere do valor do pedido ({header_price})")
            return False

        return True

    # ═══════════════════════════════════════════════════════════════════════════
    # GERAÇÃO DO JSON COMPLETO - Método principal
    # ═══════════════════════════════════════════════════════════════════════════

    def generate_json_with_header(
        self,
        header_json: Dict,                  # JSON do cabeçalho (do Hybris)
        transaction_type: str,              # "PIX", "DEBITO", "CREDITO" ou "MULTIPLAS"
        transactions_data: List[Dict]       # Lista com dados das transações
    ) -> str:
        """Gera o JSON completo baseado no cabeçalho fornecido

        Este é o método principal. Ele:
        1. Valida o cabeçalho
        2. Processa cada transação
        3. Retorna JSON formatado

        Args:
            header_json (Dict): JSON do cabeçalho do Hybris
            transaction_type (str): Tipo de transação
            transactions_data (List[Dict]): Dados das transações

        Returns:
            str: JSON formatado ou Dict com erro
        """

        # PASSO 1: Validar cabeçalho
        is_valid, errors = self.validate_header_json(header_json)
        if not is_valid:
            # Se inválido, retorna erro
            return {
                "success": False,
                "error": "Cabeçalho JSON inválido",
                "validation_errors": errors
            }

        # PASSO 2: Criar cópia do cabeçalho (para não alterar original)
        complete_order = header_json.copy()

        # PASSO 3: Garantir que status = "PAID"
        complete_order["status"] = "PAID"

        # PASSO 4: Inicializar array de transações
        complete_order["transactions"] = []

        # PASSO 5: Processar transações baseado no tipo
        transaction_type = transaction_type.upper()  # Normaliza maiúsculas

        if transaction_type == "PIX":
            # Para PIX, processa cada transação como PIX
            for trans_data in transactions_data:
                transaction = self.create_pix_transaction(
                    amount=self.format_money(trans_data.get("amount", 0)),
                    merchant_name=trans_data.get("merchant_name", ""),
                    merchant_code=trans_data.get("merchant_code", "0027822336749400"),
                    terminal_number=trans_data.get("number", trans_data.get("terminal_number", "11111111")),
                    authorization_code=trans_data.get("authorization_code"),
                    created_at=trans_data.get("created_at"),
                    preserve_payment_fields=trans_data.get("preserve_payment_fields")
                )
                complete_order["transactions"].append(transaction)

        elif transaction_type == "DEBITO":
            # Para DÉBITO, processa cada transação como DÉBITO
            # ... similar a PIX ...
            pass

        elif transaction_type == "CREDITO":
            # Para CRÉDITO, processa cada transação como CRÉDITO
            # ... similar a PIX ...
            pass

        elif transaction_type == "MULTIPLAS":
            # Para MÚLTIPLAS, processa cada transação com seu próprio tipo
            for trans_data in transactions_data:
                t_type = trans_data.get("type", "").upper()  # Tipo da transação
                # ... cria transação específica baseada em t_type ...
                pass

        # PASSO 6: Validar totais (soma deve bater)
        self.validate_transaction_totals(complete_order["price"], complete_order["transactions"])

        # PASSO 7: Converter para string JSON formatada
        return json.dumps(
            complete_order,           # Dicionário Python
            indent=2,                 # Indentação de 2 espaços
            ensure_ascii=False        # Permite acentos e caracteres especiais
        )


# ═══════════════════════════════════════════════════════════════════════════════
# FUNÇÃO PARA N8N - Compatível com Code Node do n8n
# ═══════════════════════════════════════════════════════════════════════════════

def n8n_generate_json(input_data: Dict) -> Dict:
    """Função compatível com o Code Node do n8n - VERSÃO 2.0

    Esta função envolve a classe HybrisJSONGenerator e é chamada
    pelo n8n automaticamente.

    Input esperado (input_data):
    {
        "header_json": { ... },  # JSON do cabeçalho do Hybris
        "transaction_type": "PIX|DEBITO|CREDITO|MULTIPLAS",
        "transactions": [
            {
                "amount": 100.50,
                "merchant_name": "Loja X",
                "card_mask": "************1234",  # para débito/crédito
                "card_brand": "VISA",  # para débito/crédito
                "number_of_quotas": 6,  # para crédito
                "authorization_code": "ABC123"  # para débito/crédito
            }
        ]
    }

    Returns:
        Dict: Com sucesso/erro e metadados
    """
    try:
        # Criar instância do gerador
        generator = HybrisJSONGenerator()

        # Extrair dados do input do n8n
        header_json = input_data.get("header_json", {})
        transaction_type = input_data.get("transaction_type", "")
        transactions_data = input_data.get("transactions", [])

        # Validar que todos os campos foram fornecidos
        if not header_json:
            return {"success": False, "error": "Campo 'header_json' não fornecido"}

        if not transaction_type:
            return {"success": False, "error": "Campo 'transaction_type' não fornecido"}

        if not transactions_data or len(transactions_data) == 0:
            return {"success": False, "error": "Campo 'transactions' vazio ou não fornecido"}

        # Gerar JSON usando o método principal
        json_result = generator.generate_json_with_header(
            header_json=header_json,
            transaction_type=transaction_type,
            transactions_data=transactions_data
        )

        # Se houve erro na validação
        if isinstance(json_result, dict) and not json_result.get("success", True):
            return json_result

        # Parse do JSON gerado
        json_object = json.loads(json_result)

        # Retornar resultado de sucesso com metadados
        return {
            "success": True,
            "message": "JSON gerado com sucesso!",
            "order_number": json_object["number"],
            "transaction_count": len(json_object["transactions"]),
            "total_amount": json_object["price"],  # em centavos
            "total_amount_brl": generator.parse_money(json_object["price"]),  # em reais
            "json_string": json_result,  # JSON como string
            "json_object": json_object  # JSON como objeto Python
        }

    except json.JSONDecodeError as e:
        return {"success": False, "error": "Erro ao fazer parse do JSON do cabeçalho", "details": str(e)}

    except Exception as e:
        return {"success": False, "error": "Erro ao gerar JSON", "details": str(e), "input_received": input_data}


# ═══════════════════════════════════════════════════════════════════════════════
# EXEMPLOS DE USO
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # Este bloco executa APENAS quando o arquivo é executado diretamente
    # (não quando é importado como módulo em outro arquivo)

    print("TESTANDO GERADOR V2.0 COM IDs DE 42 CARACTERES\n")

    # Testar geração de IDs
    gen = HybrisJSONGenerator()
    print("Teste de ID único:")
    id1 = gen.generate_unique_id()
    id2 = gen.generate_unique_id()
    print(f"  ID 1: {id1} (tamanho: {len(id1)})")
    print(f"  ID 2: {id2} (tamanho: {len(id2)})")
    print(f"  São diferentes: {id1 != id2}\n")
