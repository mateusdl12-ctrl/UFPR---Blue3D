@echo off
title Blus3D - Servidor e Links Personalizados
echo ========================================================
echo        INICIANDO SERVIDORES BLUS3D (ADM + CLIENTE)
echo ========================================================
echo.
echo [1/4] Iniciando Servidor ADM (porta 8501)...
start "Blus3D ADM Server" /min py -m streamlit run main.py --server.headless true --server.port 8501

echo [2/4] Iniciando Servidor CLIENTE (porta 8502)...
start "Blus3D CLIENTE Server" /min py -m streamlit run cliente_app.py --server.headless true --server.port 8502

timeout /t 4 >nul

echo [3/4] Gerando link publico ADM (https://blus3d-adm.loca.lt)...
start "Tunel ADM" cmd /c "npx -y localtunnel --port 8501 --subdomain blus3d-adm"

echo [4/4] Gerando link publico CLIENTE (https://blus3d-cliente.loca.lt)...
start "Tunel CLIENTE" cmd /c "npx -y localtunnel --port 8502 --subdomain blus3d-cliente"

echo.
echo ========================================================
echo                 LINKS DISPONIVEIS:
echo ========================================================
echo  CLIENTE : https://blus3d-cliente.loca.lt
echo  ADM     : https://blus3d-adm.loca.lt
echo ========================================================
echo.
echo Pressione qualquer tecla para encerrar esta janela.
pause >nul
