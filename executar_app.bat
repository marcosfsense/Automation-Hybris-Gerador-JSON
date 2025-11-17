@echo off
REM ========================================================
REM LAUNCHER - GERADOR DE JSON HYBRIS
REM ========================================================
REM Verifica dependencias e inicia a aplicacao
REM ========================================================

setlocal enabledelayedexpansion

cls
echo.
echo ========================================================
echo   GERADOR JSON HYBRIS - LAUNCHER
echo   Sistema de Geracao de JSONs para Pagamentos
echo ========================================================
echo.

REM ========================================================
REM VERIFICAR SE PYTHON ESTÁ INSTALADO
REM ========================================================
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Python nao esta instalado ou nao esta no PATH
    echo.
    echo Opcoes:
    echo [1] Executar instalador automatico
    echo [2] Ir para https://www.python.org/downloads/
    echo [3] Sair
    echo.
    set /p CHOICE="Escolha uma opcao (1-3): "

    if "!CHOICE!"=="1" (
        REM Procurar instalador na pasta raiz
        if exist "instalar_python.bat" (
            call instalar_python.bat
            exit /b 0
        ) else (
            echo [ERRO] Script instalador nao encontrado
            pause
            exit /b 1
        )
    ) else if "!CHOICE!"=="2" (
        start https://www.python.org/downloads/
        echo.
        echo [INFO] Apos instalar Python, execute este script novamente.
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
    echo [AVISO] Streamlit nao esta instalado
    echo.
    echo Instalando dependencias...
    echo.
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo [ERRO] Erro ao instalar dependencias
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
echo [OK] Todas as dependencias verificadas!
echo.
echo Iniciando aplicacao...
echo.
echo [INFO] O navegador abrirah automaticamente em:
echo        http://localhost:8501
echo.
echo Para parar a aplicacao, pressione Ctrl+C
echo.
echo ========================================================
echo.

cd /d "%~dp0"
python -m streamlit run src\app_streamlit.py

pause
