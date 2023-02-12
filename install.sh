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
echo "done"

# Copy
echo "Installing ..."
mv dnsmod.py "$install_path"
echo "Done! ;)"

# Permission
echo "making script executable..."
chmod +x "$install_path"
echo "done"

echo "DNSMod installed successfully!"
dnsmod help
