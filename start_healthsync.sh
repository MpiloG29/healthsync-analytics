#!/bin/bash

# HealthSync Analytics - Complete Startup Script
# Run this script to start the entire project

echo "=========================================="
echo "   HealthSync Analytics - Starting Up"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to check if a port is in use
check_port() {
    netstat -an 2>/dev/null | grep ":$1" | grep LISTEN > /dev/null
    return $?
}

# Function to kill process on port
kill_port() {
    local port=$1
    local pid=$(lsof -ti:$port 2>/dev/null)
    if [ ! -z "$pid" ]; then
        echo "Killing process on port $port (PID: $pid)"
        kill -9 $pid 2>/dev/null
        sleep 1
    fi
}

# Kill existing services
echo -e "${YELLOW}Stopping existing services...${NC}"
kill_port 8001
kill_port 8080
kill_port 9000
sleep 2

# Check Python dependencies
echo -e "${YELLOW}Checking Python dependencies...${NC}"
if ! python -c "import fastapi" 2>/dev/null; then
    echo -e "${RED}FastAPI not found. Installing...${NC}"
    pip install fastapi uvicorn
fi

# Start FastAPI Backend
echo -e "${YELLOW}Starting FastAPI backend...${NC}"
if check_port 8001; then
    echo -e "${RED}Port 8001 is already in use!${NC}"
else
    python -m uvicorn app:app --reload --host 0.0.0.0 --port 8001 > fastapi.log 2>&1 &
    FASTAPI_PID=$!
    sleep 5
    if check_port 8001; then
        echo -e "${GREEN}âœ“ FastAPI running on http://localhost:8001${NC}"
        echo -e "${GREEN}âœ“ API Docs: http://localhost:8001/docs${NC}"
    else
        echo -e "${RED}âœ— Failed to start FastAPI${NC}"
        tail -10 fastapi.log
    fi
fi

# Start HTTP Server for Dashboard
echo -e "${YELLOW}Starting Dashboard server...${NC}"
if check_port 8080; then
    echo -e "${RED}Port 8080 is already in use!${NC}"
else
    python -m http.server 8080 --bind 0.0.0.0 > httpserver.log 2>&1 &
    HTTP_PID=$!
    sleep 3
    if check_port 8080; then
        echo -e "${GREEN}âœ“ Dashboard running on http://localhost:8080${NC}"
        echo -e "${GREEN}âœ“ Main dashboard: http://localhost:8080/dashboard.html${NC}"
    else
        echo -e "${RED}âœ— Failed to start HTTP server${NC}"
        tail -10 httpserver.log
    fi
fi

# Create a simple monitoring script
cat > monitor.sh << 'MONITOR_EOF'
#!/bin/bash
echo "HealthSync Monitor"
echo "=================="
echo "1. FastAPI (API): http://localhost:8001"
echo "2. Dashboard: http://localhost:8080/dashboard.html"
echo "3. API Docs: http://localhost:8001/docs"
echo "4. Test Page: http://localhost:8080/test_dashboard_final.html"
echo ""
echo "Press Ctrl+C to stop monitoring"
echo ""
while true; do
    echo -n "."
    sleep 5
done
MONITOR_EOF

chmod +x monitor.sh

echo -e "\n${GREEN}==========================================${NC}"
echo -e "${GREEN}   HealthSync Analytics is RUNNING!${NC}"
echo -e "${GREEN}==========================================${NC}"
echo ""
echo -e "${YELLOW}Important URLs:${NC}"
echo "1. í³Š Dashboard: http://localhost:8080/dashboard.html"
echo "2. í´§ API Server: http://localhost:8001"
echo "3. í³š API Documentation: http://localhost:8001/docs"
echo "4. í·ª Test Connection: http://localhost:8080/test_dashboard_final.html"
echo ""
echo -e "${YELLOW}To stop all services, run:${NC}"
echo "pkill -f \"uvicorn.*8001\" && pkill -f \"http.server.*8080\""
echo ""
echo -e "${YELLOW}To view logs:${NC}"
echo "tail -f fastapi.log    # FastAPI logs"
echo "tail -f httpserver.log # HTTP server logs"
echo ""
echo -e "${YELLOW}Quick test:${NC}"
echo "curl http://localhost:8001/health"
echo ""
echo -e "${GREEN}Enjoy HealthSync Analytics! íº€${NC}"
