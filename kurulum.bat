@echo off
setlocal
cd /d "%~dp0"

echo [1/4] Python kontrol ediliyor...
set "PY_CMD="

where python >nul 2>nul
if %errorlevel%==0 (
    python -c "import sys; raise SystemExit(0 if sys.version_info.major==3 else 1)" >nul 2>nul
    if %errorlevel%==0 set "PY_CMD=python"
)

if not defined PY_CMD (
    where py >nul 2>nul
    if %errorlevel%==0 (
        py -3.13 -c "import sys" >nul 2>nul
        if %errorlevel%==0 (
            set "PY_CMD=py -3.13"
        ) else (
            py -3 -c "import sys" >nul 2>nul
            if %errorlevel%==0 (
                set "PY_CMD=py -3"
            ) else (
                py -c "import sys" >nul 2>nul
                if %errorlevel%==0 set "PY_CMD=py"
            )
        )
    )
)

if not defined PY_CMD (
    echo [HATA] Uygun Python 3 bulunamadi.
    echo [HATA] Python 3.13 kurup tekrar deneyin: https://www.python.org/downloads/
    exit /b 1
)

echo [2/4] Sanal ortam olusturuluyor...
if not exist ".venv\Scripts\python.exe" (
    %PY_CMD% -m venv .venv
    if not %errorlevel%==0 (
        echo [HATA] .venv olusturulamadi.
        exit /b 1
    )
)

echo [3/4] pip guncelleniyor...
call ".venv\Scripts\activate.bat"
python -m pip install --upgrade pip
if not %errorlevel%==0 (
    echo [HATA] pip guncellenemedi.
    exit /b 1
)

echo [4/4] Paketler kuruluyor...
pip install -r requirements.txt
if not %errorlevel%==0 (
    echo [HATA] Paket kurulumu basarisiz.
    exit /b 1
)

echo [OK] Kurulum tamamlandi.
exit /b 0
