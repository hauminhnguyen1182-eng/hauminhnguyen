#!/bin/bash

# Kill existing processes
pkill -f "gunicorn" 2>/dev/null
pkill -f "cloudflared" 2>/dev/null
sleep 2

# Start Flask with gunicorn
cd /workspace/chatbot
~/.local/bin/gunicorn -w 2 -b 0.0.0.0:5000 --timeout 120 app:app > /tmp/gunicorn.log 2>&1 &
GUNICORN_PID=$!
echo "Gunicorn started (PID: $GUNICORN_PID)"

# Wait for gunicorn to start
sleep 3

# Test health
if curl -s http://127.0.0.1:5000/api/health > /dev/null; then
    echo "✅ Flask API is running"
else
    echo "❌ Flask API failed to start"
    exit 1
fi

# Start cloudflared tunnel
/workspace/cloudflared tunnel --url http://127.0.0.1:5000 > /tmp/cloudflared.log 2>&1 &
TUNNEL_PID=$!
echo "Cloudflared started (PID: $TUNNEL_PID)"

# Wait for tunnel to start
sleep 10

# Get tunnel URL
TUNNEL_URL=$(grep "trycloudflare.com" /tmp/cloudflared.log | grep -o 'https://[^[:space:]]*' | head -1)
echo "Tunnel URL: $TUNNEL_URL"

# Test tunnel
if curl -s "$TUNNEL_URL/api/health" > /dev/null; then
    echo "✅ Tunnel is working"
else
    echo "❌ Tunnel failed to start"
fi

# Update chatbot.html with tunnel URL
sed -i "s|https://[^']*trycloudflare.com|$TUNNEL_URL|g" /workspace/blog/chatbot.html

echo ""
echo "=== Services Running ==="
echo "Flask API: http://127.0.0.1:5000"
echo "Tunnel: $TUNNEL_URL"
echo "Blog: https://hauminhnguyen.pages.dev/blog/chatbot"
echo ""
echo "To stop: pkill -f 'gunicorn|cloudflared'"