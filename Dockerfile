# Usar Python 3.11 slim (mais leve que a imagem padrão)
FROM python:3.11-slim

# Definir diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema (opcional, mas recomendado para evitar problemas)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    nginx \
    apache2-utils \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements.txt
COPY requirements.txt .

# Instalar dependências Python (sem cache para economizar espaço)
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY src/ ./src/
COPY img/ ./img/
COPY .streamlit/ ./.streamlit/
COPY .htpasswd /etc/nginx/.htpasswd

# Criar diretório Nginx config
RUN mkdir -p /etc/nginx/conf.d

# Criar arquivo nginx.conf com autenticação
RUN cat > /etc/nginx/conf.d/default.conf << 'EOF'
server {
    listen 80;
    server_name _;

    location / {
        auth_basic "Acesso Restrito - Autenticação Requerida";
        auth_basic_user_file /etc/nginx/.htpasswd;

        proxy_pass http://127.0.0.1:8501;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }

    location /_stcore/health {
        access_log off;
        proxy_pass http://127.0.0.1:8501;
    }
}
EOF

# Script para iniciar Nginx e Streamlit
RUN cat > /start.sh << 'EOF'
#!/bin/bash
set -e

# Iniciar Nginx em background
nginx -g "daemon off;" &
NGINX_PID=$!

# Aguardar um pouco para Nginx iniciar
sleep 2

# Iniciar Streamlit em foreground (principal)
exec streamlit run src/app_streamlit.py --server.port=8501 --server.address=127.0.0.1
EOF
RUN chmod +x /start.sh

# Expor porta padrão do Streamlit
EXPOSE 8501

# Comando para iniciar Nginx + Streamlit
CMD ["/start.sh"]
