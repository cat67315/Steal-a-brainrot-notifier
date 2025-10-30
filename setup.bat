@echo off
pip --version
if %errorlevel% neq 0 (
    echo pip is not installed, run the pithon installer first.
    echo Make shure to check the box that says "Add Python to PATH" and the box that says "Install pip"
    echo Downloading python installer...
    curl https://www.python.org/ftp/python/3.13.9/python-3.13.9-amd64.exe
    echo Starting python installer in 5 seconds...
    timeout /t 5 /nobreak >nul
    start python-3.13.9-amd64.exe
) else (
    pip install -r requirements.txt
    winget install --id UB-Mannheim.TesseractOCR -e
    echo Finished install! Run main.py to start the program.
    pause
)