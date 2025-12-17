#!/bin/bash
echo "Testing HealthSync API endpoints..."
echo "====================================="

# Test root endpoint
echo "1. Root endpoint (/):"
curl -s http://localhost:8001/ | python -m json.tool

echo -e "\n2. Health check (/health):"
curl -s http://localhost:8001/health | python -m json.tool

echo -e "\n3. Analytics data (/analytics):"
curl -s http://localhost:8001/analytics | python -m json.tool | head -20

echo -e "\n4. Patients data (/patients):"
curl -s http://localhost:8001/patients | python -m json.tool

echo -e "\n5. Test prediction (/predict):"
curl -s -X POST http://localhost:8001/predict \
  -H "Content-Type: application/json" \
  -d '{"age":65, "systolic_bp":120}' | python -m json.tool

echo -e "\n6. Test CORS endpoint (/test-cors):"
curl -s http://localhost:8001/test-cors | python -m json.tool

echo -e "\n7. Dashboard endpoint (/dashboard):"
curl -s -I http://localhost:8001/dashboard | head -5

echo -e "\n====================================="
echo "All endpoints tested!"
