#!/usr/bin/env bash
# Docker Engine + Compose plugin на Ubuntu 24.04 (DigitalOcean Droplet).
# 1GB Droplet: 2G swap до build (django-droplet-http-first).
set -euo pipefail

ensure_swap() {
  mem_kb="$(awk '/MemTotal/ {print $2}' /proc/meminfo)"
  if [ "${mem_kb}" -ge 1536000 ]; then
    return 0
  fi
  if swapon --show | grep -q .; then
    echo "==> Swap уже є"
    swapon --show
    return 0
  fi
  echo "==> RAM < 1.5G — створюємо 2G swap"
  fallocate -l 2G /swapfile
  chmod 600 /swapfile
  mkswap /swapfile
  swapon /swapfile
  if ! grep -q '^/swapfile ' /etc/fstab; then
    echo '/swapfile none swap sw 0 0' >> /etc/fstab
  fi
  swapon --show
}

ensure_ufw() {
  if ! command -v ufw >/dev/null 2>&1; then
    return 0
  fi
  ufw allow OpenSSH
  ufw allow 80/tcp
  ufw allow 443/tcp
  ufw --force enable
  ufw status
}

ensure_swap
ensure_ufw

if command -v docker >/dev/null 2>&1; then
  echo "==> Docker вже встановлено: $(docker --version)"
  docker compose version
  exit 0
fi

echo "==> Встановлення Docker через офіційний скрипт get.docker.com"
curl -fsSL https://get.docker.com | sh

systemctl enable --now docker
docker --version
docker compose version
