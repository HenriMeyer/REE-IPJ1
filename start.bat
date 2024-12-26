@echo off
if not exist "venv" (
    echo Creating virtual environment...
    python3.12 -m venv venv
) else (
    echo Virtual environment already exists.
)

echo Activate virtual environment...
call venv\Scripts\activate

echo Installing libraries...
pip install -r requirements.txt

echo Starting Python script...
cd src
python main.py

echo Deactivating virtual environment...
deactivate

pause
