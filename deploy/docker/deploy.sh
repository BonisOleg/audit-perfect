#!/usr/bin/env bash
# HTTP-first деплой Аудит-Перфект на Droplet (Docker Compose + nginx).
# SSL/домен — окремо, django-docker-ssl. Push на GitHub ≠ live.
set -euo pipefail

cd "$(dirname "$0")/../.."

COMPOSE=(docker compose)
EXPECTED_SERVICES=(db web nginx)

if [ "${1:-}" = "--pull" ]; then
  if [ -d .git ]; then
    echo "==> git pull origin main"
    git fetch origin
    git checkout main
    git pull --ff-only origin main
  else
    echo "FATAL: --pull потребує git-клону в /var/www/auditperfekt"
    exit 1
  fi
fi

if [ ! -f .env ]; then
  echo "FATAL: немає .env — створи його на сервері (секрети не з локального develop .env)"
  exit 1
fi

if grep -E '^(SECRET_KEY|POSTGRES_PASSWORD|ALLOWED_HOSTS|CSRF_TRUSTED_ORIGINS)=' .env | grep -qE 'DROPLET_IP|CHANGE_ME|change-me-in-production|dev-only-insecure'; then
  echo "FATAL: у .env лишилися плейсхолдери (DROPLET_IP / CHANGE_ME / dev-ключ)"
  exit 1
fi

if ! grep -qE 'ALLOWED_HOSTS=.*[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+' .env; then
  echo "FATAL: ALLOWED_HOSTS має містити IPv4 Droplet (не лише localhost)"
  exit 1
fi

csrf_ip="$(
  grep -E '^CSRF_TRUSTED_ORIGINS=' .env \
    | grep -oE 'http://[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+' \
    | grep -vE 'http://127\.' \
    | head -1 || true
)"
if [ -z "${csrf_ip}" ]; then
  echo "FATAL: CSRF_TRUSTED_ORIGINS має містити http://<публічний IPv4>"
  exit 1
fi

DROPLET_IP="$(
  grep -E '^ALLOWED_HOSTS=' .env \
    | grep -oE '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+' \
    | grep -vE '^127\.' \
    | head -1 || true
)"
if [ -z "${DROPLET_IP}" ]; then
  echo "FATAL: не вдалося вичитати публічний IPv4 з ALLOWED_HOSTS"
  exit 1
fi

echo "==> Звільняємо порти 80/443 від host nginx/gunicorn"
systemctl stop nginx 2>/dev/null || true
systemctl disable nginx 2>/dev/null || true
systemctl stop gunicorn 2>/dev/null || true

echo "==> Build web"
"${COMPOSE[@]}" build web

echo "==> Up (перший up нефатальний — ERR-52)"
"${COMPOSE[@]}" up -d --force-recreate || echo "WARN: перший up повернув помилку — фінальний up нижче"

echo "==> Чекаємо web /healthz/ ..."
ok=0
for _ in $(seq 1 40); do
  if "${COMPOSE[@]}" exec -T web \
    python3 -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/healthz/', timeout=2)" \
    >/dev/null 2>&1; then
    echo "==> web OK"
    ok=1
    break
  fi
  sleep 3
done
if [ "$ok" -ne 1 ]; then
  echo "FATAL: web не відповів на /healthz/ за ~2 хв"
  "${COMPOSE[@]}" logs --tail=80 web
  exit 1
fi

"${COMPOSE[@]}" up -d

echo "==> Інвентаризація сервісів (inspect Status, не grep compose ps)"
"${COMPOSE[@]}" ps
missing=0
for svc in "${EXPECTED_SERVICES[@]}"; do
  cid="$("${COMPOSE[@]}" ps -q "$svc" 2>/dev/null || true)"
  if [ -z "$cid" ]; then
    echo "WARN: сервіс відсутній: $svc"
    missing=1
    continue
  fi
  state="$(docker inspect -f '{{.State.Status}}' "$cid" 2>/dev/null || echo missing)"
  if [ "$state" != "running" ]; then
    echo "WARN: сервіс не running ($state): $svc"
    missing=1
  fi
done
if [ "$missing" -ne 0 ]; then
  echo "FATAL: не всі сервіси running"
  "${COMPOSE[@]}" logs --tail=50
  exit 1
fi

echo "==> Django check"
"${COMPOSE[@]}" exec -T web python3 manage.py check

echo "==> Smoke Host=${DROPLET_IP}"
curl -sf http://127.0.0.1/healthz/ && echo " healthz OK" || echo "WARN: healthz failed"
curl -sI -H "Host: ${DROPLET_IP}" http://127.0.0.1/ | head -5

echo "==> Далі: createsuperuser (seed уже в entrypoint, якщо контенту ще не було)"
echo "==>   docker compose exec web python manage.py createsuperuser"
echo "==> Логи: docker compose logs -f web nginx"
