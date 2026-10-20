@echo off
chcp 65001 >nul
echo ============================================
echo   Instalando el sistema de Abel
echo ============================================
echo.
echo 1) Programas (si faltan): Python, Node, ffmpeg y Git
where py >nul 2>nul || winget install -e --id Python.Python.3.12 --accept-package-agreements --accept-source-agreements
where node >nul 2>nul || winget install -e --id OpenJS.NodeJS.LTS --accept-package-agreements --accept-source-agreements
where ffmpeg >nul 2>nul || winget install -e --id Gyan.FFmpeg --accept-package-agreements --accept-source-agreements
where git >nul 2>nul || winget install -e --id Git.Git --accept-package-agreements --accept-source-agreements
echo.
echo 2) Archivos, memoria de Claude y librerias
where py >nul 2>nul && (py -3.12 "%~dp0instalar.py") || (
  echo.
  echo Python se acaba de instalar: CIERRA esta ventana y vuelve a hacer doble clic en INSTALAR.bat
)
echo.
pause
