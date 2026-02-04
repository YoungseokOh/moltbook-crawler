#!/bin/bash

# Configuration
INTERVAL=300 # 5 minutes
PYTHON_SCRIPT="api_downloader.py"

echo "=== Moltbook Auto-Collector Started ==="
echo "Interval: $INTERVAL seconds"
echo "Script: $PYTHON_SCRIPT"
echo "Press [CTRL+C] to stop.."

while true; do
    echo "[$(date)] Starting data collection..."
    python3 "$PYTHON_SCRIPT"
    
    echo "[$(date)] Collection cycle complete. Waiting for $INTERVAL seconds..."
    sleep $INTERVAL
done
