@echo off
title Blus3D - Parar Servicos
echo Parando servidores do Blus3D e tuneis...

powershell -Command "Get-NetTCPConnection -LocalPort 8501,8502 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess | ForEach-Object { Stop-Process -Id $_ -Force -ErrorAction SilentlyContinue }"
powershell -Command "Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*blus3d*' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }"

echo.
echo Servicos parados com sucesso!
timeout /t 2 >nul
