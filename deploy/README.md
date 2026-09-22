# Деплой на сервер Замовника

1. Скопіювати репозиторій на сервер, створити `.env` з production-секретами.
2. `bash deploy/docker/install-docker.sh` (якщо Docker ще немає).
3. `bash deploy/docker/deploy.sh` — HTTP по IP. Оновлення: `bash deploy/docker/deploy.sh --pull`.
4. `docker compose exec web python manage.py createsuperuser`
5. Підключити домен і SSL (certbot / `django-docker-ssl`).
6. GA4: додати `GA4_MEASUREMENT_ID` у `.env` після отримання ID від Замовника.
7. Контакти/адвокатське свідоцтво — оновити в адмінці після матеріалів клієнта.

Локально без Docker:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py seed_content
python manage.py runserver
```
