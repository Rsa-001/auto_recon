#!/bin/bash

echo "Setting up auto_recon dependencies..."

# Update system
sudo apt update

# Install required tools
echo "Installing ffuf, nmap, whatweb, jq..."
sudo apt install -y ffuf nmap whatweb

# Check and install Go (for subfinder)
if ! command -v go &> /dev/null; then
    echo "⬇️ Installing Golang..."
    sudo apt install -y golang
fi

# Install subfinder
if ! command -v subfinder &> /dev/null; then
    echo "⬇️ Installing subfinder..."
    go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
    echo 'export PATH="$PATH:$HOME/go/bin"' >> ~/.bashrc
    source ~/.bashrc
fi

# Install SecLists if not present
if [ ! -d "/usr/share/seclists" ]; then
    echo "Downloading SecLists..."
    sudo git clone https://github.com/danielmiessler/SecLists.git /usr/share/seclists
fi

echo "Setup completed. You can now run: python3 auto_recon.py <target>"
