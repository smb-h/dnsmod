#!/bin/bash

platform=`uname`

if [ "$platform" = "Linux" ]
then
    install_path="/usr/bin/dnsmod"
fi
if [ "$platform" = "Darwin" ]
then
    install_path="/usr/local/bin/dnsmod"
fi

# Download
echo "Downloading ..."
repo="smb-h/dnsmod"
tag_name=$(curl --silent https://api.github.com/repos/$repo/releases/latest \
                  | grep '"tag_name"' \
                  | sed --regexp-extended 's/.*"([^"]+)".*/\1/')
curl -sfL "https://github.com/$repo/releases/download/$tag_name/dnsmod.py" --output dnsmod.py

# Copy
echo "Installing ..."
mv dnsmod.py "$install_path"

# Permission
echo "Making script executable ..."
chmod +x "$install_path"

echo "DNSMod installed successfully!"
dnsmod -h
