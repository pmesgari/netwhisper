#!/bin/bash
set -e

# Name of your virtual environment
VENV_DIR="../netwhisper-venv"

# Path to your wheel file
WHEEL_FILE="dist/netwhisper-0.1.0-py3-none-any.whl"

# Check if virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Virtual environment $VENV_DIR does not exist. Creating with uv..."
    uv venv "$VENV_DIR"
else
    echo "Virtual environment $VENV_DIR already exists."
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# Building the package
echo "Building package..."
uv build

# Install the wheel
echo "Installing package from $WHEEL_FILE..."
uv pip install "$WHEEL_FILE"

echo "✅ Setup complete. Virtual environment '$VENV_DIR' is ready."
