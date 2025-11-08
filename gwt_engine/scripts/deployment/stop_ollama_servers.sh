#!/bin/bash
# Stop all Ollama instances

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}Stopping Ollama instances...${NC}"

stop_instance() {
    local NAME=$1
    local PID_FILE=/tmp/ollama_${NAME}.pid

    if [ -f "$PID_FILE" ]; then
        PID=$(cat $PID_FILE)
        if kill -0 $PID 2>/dev/null; then
            echo "Stopping $NAME (PID: $PID)..."
            kill $PID
            rm $PID_FILE
            echo -e "${GREEN}✓ $NAME stopped${NC}"
        else
            echo "$NAME not running"
            rm $PID_FILE
        fi
    else
        echo "$NAME PID file not found"
    fi
}

stop_instance "central"
stop_instance "gpu0_specialists"
stop_instance "gpu1_specialists"

echo ""
echo -e "${GREEN}All Ollama instances stopped${NC}"
