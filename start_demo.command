#!/bin/zsh
set -e
ROOT="$(cd "$(dirname "$0")" && pwd)"
BACKEND="$ROOT/backend"
FRONTEND="$ROOT/frontend"

if [ ! -d "$BACKEND" ] || [ ! -d "$FRONTEND" ]; then
  echo "找不到 backend 或 frontend 目录。"
  exit 1
fi

echo "启动后端..."
if [ -d "$ROOT/venv" ]; then
  source "$ROOT/venv/bin/activate"
fi
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

cleanup() {
  kill "$BACKEND_PID" 2>/dev/null || true
}
trap cleanup EXIT

echo "启动前端..."
cd "$FRONTEND"
if [ ! -d node_modules ]; then
  npm install
fi
npm run dev -- --host 0.0.0.0
