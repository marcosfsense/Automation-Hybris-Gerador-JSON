@echo off
REM ========================================================
REM INSTALADOR AUTOMATICO PYTHON + HYBRIS JSON GENERATOR
REM ========================================================
REM Este script verifica e instala Python se necessario
REM ========================================================

setlocal enabledelayedexpansion

cls
echo.
echo ========================================================
echo   GERADOR JSON HYBRIS - INSTALADOR AUTOMATICO
echo   Setup Simplificado para Windows
echo ========================================================
echo.

REM ========================================================
REM 1. VERIFICAR SE PYTHON JA ESTA INSTALADO
REM ========================================================
echo [1/4] Verificando Python...
python --version >nul 2>&1

if %errorlevel% equ 0 (
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
    echo [OK] Python !PYTHON_VERSION! encontrado!
    goto CHECK_PIP
) else (
    echo [AVISO] Python nao encontrado
    goto INSTALL_PYTHON
)

REM ========================================================
REM 2. INSTALAR PYTHON (se nao estiver)
REM ========================================================
:INSTALL_PYTHON
echo.
echo [AVISO] Python nao esta instalado. Iniciando download...
echo.
echo Opcoes:
echo [1] Download Automatico (3.11 - Recomendado)
echo [2] Ir para https://www.python.org/downloads/
echo [3] Cancelar
echo.
set /p CHOICE="Escolha uma opcao (1-3): "

if "%CHOICE%"=="1" (
    echo.
    echo Baixando Python 3.11...
    set PYTHON_URL=https://www.python.org/ftp/python/3.11.7/python-3.11.7-amd64.exe
    set PYTHON_INSTALLER=%TEMP%\python-installer.exe

    REM Usar PowerShell para baixar (mais confiavel)
    powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; (New-Object System.Net.WebClient).DownloadFile('!PYTHON_URL!', '!PYTHON_INSTALLER!')}"

    if exist "!PYTHON_INSTALLER!" (
        echo [OK] Download concluido
        echo.
        echo Iniciando instalador... (Siga as instrucoes na janela)
        echo [AVISO] IMPORTANTE: Marque "Add Python to PATH" durante instalacao!
        echo.
        timeout /t 3 /nobreak

        REM Executar instalador COM interface (RemovePath=0, PrependPath=1)
        REM AssociateFiles=1 para associar .py com Python
        "!PYTHON_INSTALLER!" InstallAllUsers=0 PrependPath=1 AssociateFiles=1

        echo.
        echo [INFO] Instalador finalizado. Aguardando 5 segundos...
        timeout /t 5 /nobreak

        REM Refreshar variáveis de ambiente
        echo [INFO] Atualizando PATH do sistema...
        REM Precisamos ativar a mudança de PATH sem reiniciar
        for /f "skip=2 tokens=3*" %%A in ('reg query "HKEY_CURRENT_USER\Environment" /v PATH 2^>nul') do set "USERPATH=%%A %%B"
        set "PATH=%PATH%;%USERPATH%"

        REM Verificar novamente
        python --version >nul 2>&1
        if !errorlevel! equ 0 (
            for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
            echo [OK] Python !PYTHON_VERSION! instalado com sucesso!
            goto CHECK_PIP
        ) else (
            echo [ERRO] Python ainda nao detectado. Verifique:
            echo   1. Se "Add Python to PATH" foi marcado durante instalacao
            echo   2. Feche e reabra este prompt de comando
            echo   3. Ou instale manualmente
            goto MANUAL_INSTALL
        )
    ) else (
        echo [ERRO] Erro ao baixar Python
        goto MANUAL_INSTALL
    )
) else if "%CHOICE%"=="2" (
    echo.
    echo Abrindo https://www.python.org/downloads/
    start https://www.python.org/downloads/
    echo.
    echo [INFO] Apos instalar, execute este script novamente.
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
    echo [OK] pip encontrado!
    goto INSTALL_DEPENDENCIES
) else (
    echo [AVISO] pip nao encontrado
    echo Tentando ativar pip...
    python -m pip --version >nul 2>&1
    if %errorlevel% equ 0 (
        echo [OK] pip ativado!
        set PIP_CMD=python -m pip
        goto INSTALL_DEPENDENCIES
    ) else (
        echo [ERRO] Erro ao ativar pip
        pause
        exit /b 1
    )
)

REM ========================================================
REM 4. INSTALAR DEPENDENCIAS
REM ========================================================
:INSTALL_DEPENDENCIES
echo.
echo [3/4] Instalando dependencias (Streamlit)...
echo.

if not defined PIP_CMD set PIP_CMD=pip

%PIP_CMD% install --upgrade pip >nul 2>&1
%PIP_CMD% install -r requirements.txt

if %errorlevel% equ 0 (
    echo [OK] Dependencias instaladas com sucesso!
) else (
    echo [ERRO] Erro ao instalar dependencias
    pause
    exit /b 1
)

REM ========================================================
REM 5. INICIAR APLICACAO
REM ========================================================
echo.
echo [4/4] Iniciando aplicacao...
echo.
echo [OK] Tudo pronto!
echo.
echo A aplicacao abrira em: http://localhost:8501
echo.
pause

python -m streamlit run src/app_streamlit.py

exit /b 0

REM ========================================================
REM INSTALACAO MANUAL
REM ========================================================
:MANUAL_INSTALL
echo.
echo ========================================================
echo   INSTALACAO MANUAL NECESSARIA
echo ========================================================
echo.
echo 1. Acesse: https://www.python.org/downloads/
echo.
echo 2. Clique em "Download Python 3.11" (ou versao mais recente)
echo.
echo 3. Execute o instalador
echo.
echo 4. [AVISO] MARQUE: "Add Python to PATH"
echo.
echo 5. Clique em "Install Now"
echo.
echo 6. Apos a instalacao, execute este script novamente
echo.
pause
exit /b 0
