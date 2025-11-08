#!/bin/bash
# Stop all vLLM servers

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}Stopping vLLM servers...${NC}"

stop_server() {
    local NAME=$1
    local PID_FILE=/tmp/vllm_${NAME}.pid

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

stop_server "central_workspace"
stop_server "gpu1_specialists"
stop_server "gpu2_specialists"

echo ""
echo -e "${GREEN}All servers stopped${NC}"
