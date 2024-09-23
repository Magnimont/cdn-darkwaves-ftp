#!/bin/bash

# Login to the VPS without password prompt
sudo -n true
if [ $? -ne 0 ]; then
    echo "Passwordless sudo is not configured. Please configure passwordless sudo for the current user."
    exit 1
fi

# Stash any local changes to avoid conflicts during pull
echo "Stashing local changes..."
git stash &>/dev/null

# Pull the latest changes from the remote repository
echo "Pulling the latest changes from the repository..."
git pull &>/dev/null

# Check if pyenv is installed
if ! command -v pyenv &> /dev/null; then
    echo "pyenv is not installed. Please install pyenv first."
    exit 1
fi

# Create a new virtual environment with pyenv
PYTHON_VERSION="3.8.10"  # Specify your desired Python version
ENV_NAME="myenv"          # Specify your environment name

echo "Creating a virtual environment with pyenv..."
pyenv install -s $PYTHON_VERSION
pyenv virtualenv $PYTHON_VERSION $ENV_NAME

# Activate the virtual environment
echo "Activating the virtual environment..."
eval "$(pyenv init --path)"
pyenv activate $ENV_NAME

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt &>/dev/null

# Run the Flask application
echo "Starting the Flask application..."
python3 cdn.py
