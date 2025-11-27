# Usar Python 3.11 slim (mais leve que a imagem padrão)
FROM python:3.11-slim

# Definir diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema (opcional, mas recomendado para evitar problemas)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements.txt
COPY requirements.txt .

# Instalar dependências Python (sem cache para economizar espaço)
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY src/ ./src/
COPY img/ ./img/
COPY .streamlit/ ./.streamlit/

# NOTA: credentials.json e config.yaml NÃO são copiados porque:
# 1. Contêm senhas e dados sensíveis
# 2. São criados automaticamente pelo app na primeira execução
# 3. Usuários devem configurar suas próprias credenciais
# 4. Usar os arquivos .TEMPLATE como referência

# Copiar arquivos template como referência (opcional)
COPY credentials.json.TEMPLATE .
COPY config.yaml.TEMPLATE .

# Expor porta padrão do Streamlit
EXPOSE 8501

# Comando para iniciar a aplicação
CMD ["streamlit", "run", "src/app_streamlit.py", "--server.port=8501", "--server.address=0.0.0.0"]
