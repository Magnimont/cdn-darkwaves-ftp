#!/bin/bash

# login to the VPS without password prompt
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

# Ensure Python3, pip, and virtualenv are installed
echo "Checking for Python3, pip, and virtualenv..."
sudo apt update &>/dev/null
sudo apt install -y python3 python3-pip python3-venv &>/dev/null

# Create a virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating a virtual environment..."
    python3 -m venv venv &>/dev/null
fi

# Activate the virtual environment
echo "Activating the virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip &>/dev/null
pip install -r requirements.txt &>/dev/null
pip install flask

# Run the Flask application
echo "Starting the Flask application..."
python3 cdn.py

# Deactivate the virtual environment when done
deactivate
