# Аудит-Перфект

Корпоративний сайт аудиторської фірми. Стек: Django 5 + HTMX + plain CSS + Docker/nginx.

## Швидкий старт

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py seed_content
python manage.py runserver
```

Адмінка: `/admin/` (спочатку `createsuperuser`).

## Структура

- `config/` — settings (base/develop/production/test)
- `src/core` — SiteSettings, SiteBlock, static (CSS/JS/WebP)
- `src/services` — 7 послуг + 301 критичності
- `src/news`, `src/team`, `src/pages`
- `mockup/` — затверджений HTML-макет
- `docs/` — ТЗ, карта, Правки 1
- `deploy/` — nginx + інструкція деплою

Фото команди/сертифікатів у static — **WebP** (`scripts/convert_static_webp.py`).
