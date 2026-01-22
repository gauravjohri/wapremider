#!/bin/bash
set -e

echo "🚀 Starting deployment..."

# ---------- CONFIG ----------
BRANCH="main"
WORKER_SERVICE="wapreminder-worker"
API_SERVICE="wapreminder-api"
LOG_FILE="/var/log/wapreminder-deploy.log"
# ----------------------------

exec > >(tee -a $LOG_FILE) 2>&1

echo "📅 $(date)"

# 1️⃣ Make sure we are inside a git repo
if [ ! -d ".git" ]; then
  echo "❌ ERROR: Not a git repository"
  exit 1
fi

# 2️⃣ Pull latest code
echo "📥 Pulling latest code from $BRANCH..."
git pull origin $BRANCH

# 3️⃣ Check systemctl exists
if ! command -v systemctl &> /dev/null; then
  echo "❌ ERROR: systemctl not found"
  exit 1
fi

# 4️⃣ Restart worker service
echo "🔄 Restarting $WORKER_SERVICE..."
if systemctl list-units --full -all | grep -Fq "$WORKER_SERVICE.service"; then
  sudo systemctl restart $WORKER_SERVICE
  sudo systemctl status $WORKER_SERVICE --no-pager
else
  echo "⚠️ WARNING: $WORKER_SERVICE service not found"
fi

# 5️⃣ Restart API service
echo "🔄 Restarting $API_SERVICE..."
if systemctl list-units --full -all | grep -Fq "$API_SERVICE.service"; then
  sudo systemctl restart $API_SERVICE
  sudo systemctl status $API_SERVICE --no-pager
else
  echo "⚠️ WARNING: $API_SERVICE service not found"
fi

echo "✅ Deployment completed successfully"
