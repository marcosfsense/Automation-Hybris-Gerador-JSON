@echo off
REM ========================================================
REM CRIAR EXECUTÁVEL PORTÁTIL COM PYINSTALLER
REM ========================================================
REM Este script cria um .exe standalone da aplicação
REM Resultado: Um único arquivo .exe que roda sem Python
REM ========================================================

setlocal enabledelayedexpansion

echo.
echo ╔══════════════════════════════════════════════════════╗
echo ║   GERADOR JSON HYBRIS - COMPILADOR EXE              ║
echo ║   Criar Executável Portátil (sem Python)            ║
echo ╚══════════════════════════════════════════════════════╝
echo.

REM ========================================================
REM VERIFICAR DEPENDÊNCIAS
REM ========================================================
echo [1/3] Verificando dependências...
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ✗ ERRO: Python não está instalado
    echo.
    echo Instale Python primeiro: instalar_python.bat
    pause
    exit /b 1
)

echo ✓ Python encontrado

pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  PyInstaller não encontrado
    echo.
    echo Instalando PyInstaller...
    pip install pyinstaller
    if %errorlevel% neq 0 (
        echo ✗ Erro ao instalar PyInstaller
        pause
        exit /b 1
    )
)

echo ✓ PyInstaller encontrado

REM ========================================================
REM INSTALAR DEPENDÊNCIAS DO PROJETO
REM ========================================================
echo.
echo [2/3] Verificando dependências do projeto...
echo.

pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ✗ Erro ao instalar dependências
    pause
    exit /b 1
)

echo ✓ Dependências instaladas

REM ========================================================
REM CRIAR EXECUTÁVEL
REM ========================================================
echo.
echo [3/3] Compilando executável...
echo.
echo Isso pode levar 2-5 minutos...
echo.

REM Executar PyInstaller
pyinstaller ^
    --name "Gerador_JSON_Hybris" ^
    --onefile ^
    --windowed ^
    --icon=docs/logo_S2.png ^
    --add-data "src:src" ^
    --add-data "requirements.txt:." ^
    --hidden-import=streamlit ^
    --hidden-import=streamlit.web ^
    --distpath "./dist_app" ^
    "src/app_streamlit.py"

if %errorlevel% equ 0 (
    echo.
    echo ✓ Executável criado com sucesso!
    echo.
    echo Arquivo: dist_app\Gerador_JSON_Hybris.exe
    echo.
    echo Você pode distribuir este arquivo para outros usuários.
    echo Ele funciona sem precisar instalar Python!
    echo.
    pause
) else (
    echo.
    echo ✗ Erro ao compilar
    pause
    exit /b 1
)

REM ========================================================
REM LIMPEZA
REM ========================================================
echo.
echo Limpando arquivos temporários...
if exist "build" rmdir /s /q "build" >nul 2>&1
if exist "Gerador_JSON_Hybris.spec" del /q "Gerador_JSON_Hybris.spec" >nul 2>&1

echo ✓ Pronto!
echo.
echo Próximos passos:
echo 1. O arquivo .exe está em: dist_app\Gerador_JSON_Hybris.exe
echo 2. Você pode mover/copiar para qualquer lugar
echo 3. Duplo clique para executar (sem precisar de Python!)
echo.

pause
