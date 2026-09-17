# Деплой на сервер Замовника

1. Скопіювати репозиторій на сервер, створити `.env` з production-секретами.
2. `docker compose up -d --build`
3. `docker compose exec web python manage.py createsuperuser`
4. Підключити домен і SSL (certbot / `django-docker-ssl`).
5. GA4: додати `GA4_MEASUREMENT_ID` у `.env` після отримання ID від Замовника.
6. Контакти/адвокатське свідоцтво — оновити в адмінці після матеріалів клієнта.

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
