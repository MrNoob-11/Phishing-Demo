
#!/bin/bash

PROJECT="$HOME/Desktop/PhishingDemoFresh"
LOG_FILE="/tmp/phishing-demo-cloudflared.log"

cd "$PROJECT" || exit 1
source .venv/bin/activate || exit 1

SERVER_PID=""
TUNNEL_PID=""

cleanup() {
    echo "Stopping demo..."
    [ -n "$TUNNEL_PID" ] && kill "$TUNNEL_PID" 2>/dev/null
    [ -n "$SERVER_PID" ] && kill "$SERVER_PID" 2>/dev/null
    wait 2>/dev/null
}

trap cleanup EXIT INT TERM

echo "Starting Flask..."
python app.py &
SERVER_PID=$!

echo "Waiting for Flask..."
for i in {1..20}; do
    if ! kill -0 "$SERVER_PID" 2>/dev/null; then
        echo "Flask exited early. Check the error above."
        exit 1
    fi

    if curl -fsS http://127.0.0.1:5000/ >/dev/null; then
        break
    fi
    sleep 1
done

if ! curl -fsS http://127.0.0.1:5000/ >/dev/null; then
    echo "Flask did not respond on port 5000."
    exit 1
fi

echo "Starting Cloudflare tunnel..."
: > "$LOG_FILE"
cloudflared tunnel --url http://127.0.0.1:5000 > "$LOG_FILE" 2>&1 &
TUNNEL_PID=$!

echo "Waiting for Cloudflare URL..."
URL=""
for i in {1..30}; do
    URL=$(grep -Eo 'https://[a-zA-Z0-9-]+\.trycloudflare\.com' "$LOG_FILE" | head -n 1)

    if [ -n "$URL" ]; then
        break
    fi

    if ! kill -0 "$TUNNEL_PID" 2>/dev/null; then
        echo "Cloudflare exited. Check $LOG_FILE"
        exit 1
    fi

    sleep 1
done

if [ -n "$URL" ]; then
    echo ""
    echo "Training demo URL: $URL"
    open "$URL"
else
    echo "Cloudflare URL not found. Check $LOG_FILE"
fi

echo "Press Control+C to stop the demo."
wait "$SERVER_PID"
#!/bin/bash

PROJECT="$HOME/Desktop/PhishingDemoFresh"
LOG_FILE="/tmp/phishing-demo-cloudflared.log"

cd "$PROJECT" || exit 1
source .venv/bin/activate || exit 1

cleanup() {
    echo "Stopping demo..."
    [ -n "$TUNNEL_PID" ] && kill "$TUNNEL_PID" 2>/dev/null
    [ -n "$SERVER_PID" ] && kill "$SERVER_PID" 2>/dev/null
    wait 2>/dev/null
}
trap cleanup EXIT INT TERM

# Start Python
python app.py &
SERVER_PID=$!

# Wait until Flask responds
for i in {1..20}; do
    if curl -fsS http://127.0.0.1:5000/ >/dev/null; then
        break
    fi
    sleep 1
done

if ! curl -fsS http://127.0.0.1:5000/ >/dev/null; then
    echo "Flask failed to start. Check the Python error above."
    exit 1
fi

# Start Cloudflare
cloudflared tunnel --url http://127.0.0.1:5000 > "$LOG_FILE" 2>&1 &
TUNNEL_PID=$!

echo "Waiting for Cloudflare URL..."
for i in {1..30}; do
    URL=$(grep -Eo 'https://[a-zA-Z0-9-]+\.trycloudflare\.com' "$LOG_FILE" | head -n 1)
    [ -n "$URL" ] && break
    sleep 1
done

if [ -n "$URL" ]; then
    echo ""
    echo "Training demo URL: $URL"
    open "$URL"
else
    echo "Cloudflare URL not found. Check $LOG_FILE"
fi

echo "Both services are running. Press Control+C to stop."
wait "$SERVER_PID"
