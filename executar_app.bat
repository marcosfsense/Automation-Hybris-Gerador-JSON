@echo off
REM ========================================================
REM LAUNCHER - GERADOR DE JSON HYBRIS
REM ========================================================
REM Verifica dependências e inicia a aplicação
REM ========================================================

setlocal enabledelayedexpansion

echo.
echo ╔══════════════════════════════════════════════════════╗
echo ║   GERADOR JSON HYBRIS - LAUNCHER                     ║
echo ║   Sistema de Geração de JSONs para Pagamentos        ║
echo ╚══════════════════════════════════════════════════════╝
echo.

REM ========================================================
REM VERIFICAR SE PYTHON ESTÁ INSTALADO
REM ========================================================
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ✗ ERRO: Python não está instalado ou não está no PATH
    echo.
    echo Opções:
    echo [1] Executar instalador automático
    echo [2] Ir para https://www.python.org/downloads/
    echo [3] Sair
    echo.
    set /p CHOICE="Escolha uma opção (1-3): "

    if "!CHOICE!"=="1" (
        REM Procurar instalador na pasta raiz
        if exist "instalar_python.bat" (
            call instalar_python.bat
            exit /b 0
        ) else (
            echo ✗ Script instalador não encontrado
            pause
            exit /b 1
        )
    ) else if "!CHOICE!"=="2" (
        start https://www.python.org/downloads/
        echo.
        echo ℹ️  Após instalar Python, execute este script novamente.
        pause
        exit /b 0
    ) else (
        exit /b 0
    )
)

REM ========================================================
REM VERIFICAR SE STREAMLIT ESTÁ INSTALADO
REM ========================================================
python -m pip show streamlit >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Streamlit não está instalado
    echo.
    echo Instalando dependências...
    echo.
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ✗ Erro ao instalar dependências
        echo.
        echo Tente manualmente:
        echo   pip install -r requirements.txt
        pause
        exit /b 1
    )
)

REM ========================================================
REM INICIAR APLICAÇÃO
REM ========================================================
echo.
echo ✓ Todas as dependências verificadas!
echo.
echo Iniciando aplicação...
echo.
echo ℹ️  O navegador abrirá automaticamente em:
echo    http://localhost:8501
echo.
echo Para parar a aplicação, pressione Ctrl+C
echo.
echo ════════════════════════════════════════════════════════
echo.

cd /d "%~dp0"
python -m streamlit run src\app_streamlit.py

pause
