@echo off
winget install Python.Python.3
pip install -r requirements.txt
winget install --id UB-Mannheim.TesseractOCR -e
echo You just got hacked!
pause