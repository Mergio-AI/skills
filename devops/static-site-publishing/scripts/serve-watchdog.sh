#!/bin/bash
# Watchdog: keep serve.py running
# Cron job runs this every 1m. Exit 0 with empty stdout = silent (all OK).
# Prints message only when restart was needed.
#
# Usage: set STATIC_ROOT and run from the directory containing serve.py

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SERVE_PY="$SCRIPT_DIR/serve.py"

if pgrep -f "python3.*serve.py" > /dev/null 2>&1; then
    exit 0
fi

echo "🔧 serve.py crashed, restarting..."
cd "$SCRIPT_DIR" && nohup python3 serve.py > /dev/null 2>&1 &
sleep 1
if pgrep -f "python3.*serve.py" > /dev/null 2>&1; then
    echo "✅ serve.py restarted"
else
    echo "❌ serve.py restart failed"
fi
