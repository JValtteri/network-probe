#!/bin/bash

set -euxo pipefail

echo "Installing network-probe service..."
sudo cp network-probe.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable network-probe

echo "Starting network-probe service..."
sudo systemctl start network-probe

echo "Done."

