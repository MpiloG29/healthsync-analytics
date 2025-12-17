#!/bin/bash
echo "Testing HealthSync API..."
echo ""

# Test root endpoint
echo "1. Testing root endpoint:"
curl -s http://localhost:8001 | python -m json.tool
echo ""

# Test health endpoint
echo "2. Testing health check:"
curl -s http://localhost:8001/health | python -m json.tool
echo ""

# Test patients
echo "3. Testing patients endpoint:"
curl -s http://localhost:8001/patients | python -m json.tool
echo ""

echo "✅ API is working!"
