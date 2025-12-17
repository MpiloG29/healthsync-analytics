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
