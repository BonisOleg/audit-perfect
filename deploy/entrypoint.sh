#!/usr/bin/env bash
set -euo pipefail

echo "==> Waiting for PostgreSQL..."
python <<'PY'
import os, sys, time
import psycopg2
url = os.environ.get("DATABASE_URL", "")
if not url:
    sys.exit(0)
for i in range(30):
    try:
        psycopg2.connect(url)
        print("==> DB ready")
        break
    except psycopg2.OperationalError:
        time.sleep(2)
else:
    print("FATAL: DB not ready")
    sys.exit(1)
PY

echo "==> Django migrate + collectstatic"
python manage.py migrate --noinput
if python manage.py shell -c "import sys; from src.core.models import SiteSettings; sys.exit(0 if SiteSettings.objects.exists() else 1)"; then
  echo "==> seed skipped (content exists)"
else
  python manage.py seed_content
fi
python manage.py collectstatic --noinput

_static_count=$(find "${STATIC_ROOT:-/app/staticfiles}" -type f 2>/dev/null | wc -l | tr -d ' ')
echo "==> static files: ${_static_count}"

exec "$@"
