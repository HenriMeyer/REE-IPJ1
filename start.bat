@echo off

ver | findstr /i "Windows" > nul
if %errorlevel% == 0 (
    echo Running on Windows...
    mkdir "output"
    mkdir "output\Excel"
    mkdir "output\CSV"
) else (
    echo Running on macOS/Linux...
    bash -c "mkdir -p output"
    bash -c "mkdir -p output/CSV"
    bash -c "mkdir -p output/Excel"
)

if not exist "venv" (
    echo Creating virtual environment...
    python3.12 -m venv venv
) else (
    echo Virtual environment already exists.
)

echo Activate virtual environment...
call venv\Scripts\activate.bat

echo Installing libraries...
pip install -r requirements.txt

echo Starting Python script...
cd src
python main.py

echo Deactivating virtual environment...
deactivate

pause
