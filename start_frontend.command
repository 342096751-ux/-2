#!/bin/zsh
cd "$(dirname "$0")/frontend" || exit 1
if [ ! -d node_modules ]; then
  echo "Installing frontend dependencies..."
  npm install
fi
npm run dev -- --host 0.0.0.0
