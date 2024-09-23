#!/bin/bash

# login to the vps without password prompt
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

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt &>/dev/null

# Run the Flask application
echo "Starting the Flask application..."
python3 cdn.py
