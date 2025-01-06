#!/bin/bash

if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Running on macOS..."
    mkdir -p output
else
    echo "Running on Linux..."
    mkdir -p output
fi

echo "Checking for virtual environment..."

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3.12 -m venv venv
else
    echo "Virtual environment already exists."
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing libraries..."
pip install -r requirements.txt

echo "Starting Python script..."
cd src
python main.py

echo "Deactivating virtual environment..."
cd ..
deactivate

echo "Script execution completed."