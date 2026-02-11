#!/bin/bash

# Move to the folder where this script is located
#cd "$(dirname "$0")"

# 1. Function to clean up when the script stops
cleanup() {
    echo ""
    echo "🛑 Shutting down containers..."
    docker-compose down
    exit
}

# 2. Set the 'Trap' (Triggers cleanup on Ctrl+C or closing window)
trap cleanup INT TERM EXIT

echo "🚀 Starting MITM System..."

# 3. Start containers and show logs (No -d so the window stays active)
docker-compose up --build &

# 4. Wait a few seconds then open the browser
sleep 4
open http://http://0.0.0.0:8000

# Keep the script alive so the trap can catch the close event
wait