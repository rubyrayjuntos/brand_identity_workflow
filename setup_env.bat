@echo off
echo Setting up Python 3.12 virtual environment...

REM Create virtual environment
"C:\Users\raycs\AppData\Local\Programs\Python\Python312\python.exe" -m venv venv312

REM Activate virtual environment
call venv312\Scripts\activate.bat

REM Upgrade pip
python -m pip install --upgrade pip

echo Virtual environment created and activated!
echo To activate in the future, run: venv312\Scripts\activate.bat
echo To deactivate, run: deactivate

pause 