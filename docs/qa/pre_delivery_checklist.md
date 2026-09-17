# Pre-delivery E2E (локально)

- [x] `/` — головна, hero WebP, 7 напрямів, 3 переваги, новини
- [x] `/pro-nas/` — команда 8, сертифікати, кейси, Organization JSON-LD
- [x] `/poslugy/` + 7 slug
- [x] 301 `/poslugy/pryznachennya-krytychnosti/` → військовий облік
- [x] `/novyny/` + деталь статті
- [x] `/kontakty/`, `/polityka-konfidentsiynosti/`
- [x] `/sitemap.xml`, `/robots.txt`
- [x] Футер: лінк PrometeyLabs лише на homepage
- [x] CTA call / mail без Lead-форм
- [ ] Реальні контакти від Замовника
- [ ] Адвокатське свідоцтво
- [ ] GA4 ID
- [ ] Деплой на сервер Замовника + SSL
- [ ] Адаптив 320–1920 / iOS Safari (ручна перевірка на проді)

Команди перевірки:

```bash
curl -sI http://127.0.0.1:8000/poslugy/pryznachennya-krytychnosti/ | head -5
curl -s http://127.0.0.1:8000/robots.txt
curl -s http://127.0.0.1:8000/sitemap.xml | head -20
```
