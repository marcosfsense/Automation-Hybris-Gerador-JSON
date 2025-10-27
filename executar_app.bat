@echo off
echo ================================================
echo   GERADOR DE JSON - SISTEMA HYBRIS V2.0
echo ================================================
echo.
echo Iniciando aplicativo Streamlit...
echo.
echo O navegador ira abrir automaticamente em:
echo http://localhost:8501
echo.
echo Para parar o servidor, pressione Ctrl+C
echo.
echo ================================================
echo.

cd /d "%~dp0"
streamlit run src\app_streamlit.py

pause
