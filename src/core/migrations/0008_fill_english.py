from django.db import migrations

from src.core.content_en import CASE_EN, CERT_EN, NEWS_EN, SERVICE_EN, TEAM_EN


def _meta_title(title: str) -> str:
    suffix = " — Аудит-Перфект"
    full = f"{title}{suffix}"
    if len(full) <= 70:
        return full
    return f"{title[: 70 - len(suffix)].rstrip()}{suffix}"


def _meta_description(text: str) -> str:
    text = (text or "").strip()
    return text[:160]


def fill_english(apps, schema_editor):
    Service = apps.get_model("services", "Service")
    for slug, data in SERVICE_EN.items():
        Service.objects.filter(slug=slug).update(
            title_en=data["title"],
            short_description_en=data["short_description"],
            audience_en=data["audience"],
            composition_en=data["composition"],
            meta_title_en=_meta_title(data["title"]),
            meta_description_en=_meta_description(data["short_description"]),
        )

    News = apps.get_model("news", "News")
    for slug, data in NEWS_EN.items():
        News.objects.filter(slug=slug).update(
            title_en=data["title"],
            excerpt_en=data["excerpt"],
            body_en=data["body"],
            meta_title_en=_meta_title(data["title"]),
            meta_description_en=_meta_description(data["excerpt"]),
        )

    TeamMember = apps.get_model("team", "TeamMember")
    for name, role in TEAM_EN.items():
        TeamMember.objects.filter(name=name).update(role_en=role)

    Case = apps.get_model("team", "Case")
    for title_uk, data in CASE_EN.items():
        Case.objects.filter(title_uk=title_uk).update(
            title_en=data["title"],
            industry_en=data["industry"],
            result_en=data["result"],
        )

    Certificate = apps.get_model("pages", "Certificate")
    for title_uk, title_en in CERT_EN.items():
        Certificate.objects.filter(title_uk=title_uk).update(title_en=title_en)


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0007_bilingual_en"),
        ("pages", "0006_bilingual_en"),
        ("services", "0002_bilingual_en"),
        ("news", "0002_bilingual_en"),
        ("team", "0004_bilingual_en"),
    ]

    operations = [
        migrations.RunPython(fill_english, migrations.RunPython.noop),
    ]
