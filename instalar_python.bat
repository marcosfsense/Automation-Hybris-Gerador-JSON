@echo off
REM ========================================================
REM INSTALADOR AUTOMÁTICO PYTHON + HYBRIS JSON GENERATOR
REM ========================================================
REM Este script verifica e instala Python se necessário
REM ========================================================

setlocal enabledelayedexpansion

echo.
echo ╔══════════════════════════════════════════════════════╗
echo ║   GERADOR JSON HYBRIS - INSTALADOR AUTOMÁTICO        ║
echo ║   Setup Simplificado para Windows                    ║
echo ╚══════════════════════════════════════════════════════╝
echo.

REM ========================================================
REM 1. VERIFICAR SE PYTHON JÁ ESTÁ INSTALADO
REM ========================================================
echo [1/4] Verificando Python...
python --version >nul 2>&1

if %errorlevel% equ 0 (
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
    echo ✓ Python !PYTHON_VERSION! encontrado!
    goto CHECK_PIP
) else (
    echo ✗ Python não encontrado
    goto INSTALL_PYTHON
)

REM ========================================================
REM 2. INSTALAR PYTHON (se não estiver)
REM ========================================================
:INSTALL_PYTHON
echo.
echo ⚠️  Python não está instalado. Iniciando download...
echo.
echo Opções:
echo [1] Download Automático (3.11 - Recomendado)
echo [2] Ir para https://www.python.org/downloads/
echo [3] Cancelar
echo.
set /p CHOICE="Escolha uma opção (1-3): "

if "%CHOICE%"=="1" (
    echo.
    echo Baixando Python 3.11...
    set PYTHON_URL=https://www.python.org/ftp/python/3.11.7/python-3.11.7-amd64.exe
    set PYTHON_INSTALLER=%TEMP%\python-installer.exe

    REM Usar PowerShell para baixar (mais confiável)
    powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; (New-Object System.Net.WebClient).DownloadFile('!PYTHON_URL!', '!PYTHON_INSTALLER!')}"

    if exist "!PYTHON_INSTALLER!" (
        echo ✓ Download concluído
        echo.
        echo Iniciando instalador... (Siga as instruções na janela)
        echo ⚠️  IMPORTANTE: Marque "Add Python to PATH" durante instalação!
        echo.
        timeout /t 3 /nobreak

        REM Executar instalador
        "!PYTHON_INSTALLER!" /quiet PrependPath=1

        echo.
        echo ✓ Instalação concluída!
        timeout /t 3 /nobreak

        REM Verificar novamente
        python --version >nul 2>&1
        if !errorlevel! equ 0 (
            echo ✓ Python instalado com sucesso!
            goto CHECK_PIP
        ) else (
            echo ✗ Erro na instalação. Tente instalador manual.
            goto MANUAL_INSTALL
        )
    ) else (
        echo ✗ Erro ao baixar Python
        goto MANUAL_INSTALL
    )
) else if "%CHOICE%"=="2" (
    echo.
    echo Abrindo https://www.python.org/downloads/
    start https://www.python.org/downloads/
    echo.
    echo ℹ️  Após instalar, execute este script novamente.
    pause
    exit /b 0
) else (
    echo Cancelado.
    exit /b 0
)

REM ========================================================
REM 3. VERIFICAR PIP
REM ========================================================
:CHECK_PIP
echo.
echo [2/4] Verificando pip...
pip --version >nul 2>&1

if %errorlevel% equ 0 (
    echo ✓ pip encontrado!
    goto INSTALL_DEPENDENCIES
) else (
    echo ✗ pip não encontrado
    echo Tentando ativar pip...
    python -m pip --version >nul 2>&1
    if %errorlevel% equ 0 (
        echo ✓ pip ativado!
        set PIP_CMD=python -m pip
        goto INSTALL_DEPENDENCIES
    ) else (
        echo ✗ Erro ao ativar pip
        pause
        exit /b 1
    )
)

REM ========================================================
REM 4. INSTALAR DEPENDÊNCIAS
REM ========================================================
:INSTALL_DEPENDENCIES
echo.
echo [3/4] Instalando dependências (Streamlit)...
echo.

if not defined PIP_CMD set PIP_CMD=pip

%PIP_CMD% install --upgrade pip >nul 2>&1
%PIP_CMD% install -r requirements.txt

if %errorlevel% equ 0 (
    echo ✓ Dependências instaladas com sucesso!
) else (
    echo ✗ Erro ao instalar dependências
    pause
    exit /b 1
)

REM ========================================================
REM 5. INICIAR APLICAÇÃO
REM ========================================================
echo.
echo [4/4] Iniciando aplicação...
echo.
echo ✓ Tudo pronto!
echo.
echo A aplicação abrirá em: http://localhost:8501
echo.
pause

streamlit run src/app_streamlit.py

exit /b 0

REM ========================================================
REM INSTALAÇÃO MANUAL
REM ========================================================
:MANUAL_INSTALL
echo.
echo ========================================================
echo   INSTALAÇÃO MANUAL NECESSÁRIA
echo ========================================================
echo.
echo 1. Acesse: https://www.python.org/downloads/
echo.
echo 2. Clique em "Download Python 3.11" (ou versão mais recente)
echo.
echo 3. Execute o instalador
echo.
echo 4. ⚠️  MARQUE: "Add Python to PATH"
echo.
echo 5. Clique em "Install Now"
echo.
echo 6. Após a instalação, execute este script novamente
echo.
pause
exit /b 0
