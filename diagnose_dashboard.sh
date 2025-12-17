#!/bin/bash
echo "=== HealthSync Dashboard Diagnostic ==="
echo "Time: $(date)"
echo ""

# Check if servers are running
echo "1. Checking servers:"
echo "   - FastAPI (port 8001): $(netstat -an 2>/dev/null | grep ':8001' | grep LISTEN | wc -l) listeners"
echo "   - HTTP server (port 8080): $(netstat -an 2>/dev/null | grep ':8080' | grep LISTEN | wc -l) listeners"

# Check dashboard.html JavaScript
echo -e "\n2. Checking dashboard.html JavaScript:"
echo "   API_URL in dashboard.html: $(grep "const API_URL" dashboard.html)"
echo "   Fetch calls found: $(grep -c "fetch(" dashboard.html)"

# Test API connectivity from bash
echo -e "\n3. Testing API from command line:"
echo "   Analytics endpoint:"
curl -s -o /dev/null -w "Status: %{http_code}, Time: %{time_total}s\n" http://localhost:8001/analytics

echo "   Predict endpoint:"
curl -s -o /dev/null -X POST -H "Content-Type: application/json" \
  -d '{"age":65,"systolic_bp":120}' \
  -w "Status: %{http_code}, Time: %{time_total}s\n" \
  http://localhost:8001/predict

# Check CORS headers
echo -e "\n4. Checking CORS headers:"
curl -s -I -X OPTIONS http://localhost:8001/analytics | grep -i "access-control"

# Create a simple test
echo -e "\n5. Creating browser test command:"
echo "   Open in browser and check Console (F12):"
echo "   - http://localhost:8080/dashboard.html"
echo "   - Look for CORS errors"
echo "   - Look for failed fetch requests"
