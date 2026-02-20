@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\pythonw.exe" (
    echo [INFO] Sanal ortam bulunamadi. Ilk kurulum baslatiliyor...
    call "%~dp0kurulum.bat"
    if not %errorlevel%==0 (
        echo [HATA] Kurulum basarisiz. Program baslatilamadi.
        pause
        exit /b 1
    )
)

call ".venv\Scripts\activate.bat"
start "AI Asistan" /B ".venv\Scripts\pythonw.exe" "%~dp0main.pyw"
exit /b 0
