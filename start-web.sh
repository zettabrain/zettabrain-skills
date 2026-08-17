#!/bin/bash
# Start ZettaBrain Skills Web Application

echo "🚀 Starting 3RVA Quote Generator Web App..."
echo ""
echo "Access the app at:"
echo "  Local:    http://localhost:8000"
echo "  Network:  http://$(hostname -I | awk '{print $1}'):8000"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Set environment
export OLLAMA_TIMEOUT=900

# Start the web app
cd "$(dirname "$0")"
python3 -m uvicorn zettabrain_skills.web.app:app --host 0.0.0.0 --port 8000 --reload
