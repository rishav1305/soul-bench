#!/bin/bash
set -euo pipefail

echo "Installing asciinema..."
sudo apt install -y asciinema

echo "Installing agg v1.7.0 (aarch64)..."
sudo curl -L -o /usr/local/bin/agg \
  https://github.com/asciinema/agg/releases/download/v1.7.0/agg-aarch64-unknown-linux-gnu
sudo chmod +x /usr/local/bin/agg

echo "Verifying..."
asciinema --version
agg --version
echo "Done."
