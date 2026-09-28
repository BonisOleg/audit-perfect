from django.db import migrations, models


def _rewrite(value):
    if not isinstance(value, str) or not value:
        return value
    return value.replace("Audit-Perfect", "AUDYT-PERFECT").replace(
        "Аудит-Перфект", "AUDYT-PERFECT"
    )


def _rewrite_json(value):
    if isinstance(value, list):
        return [_rewrite_json(item) for item in value]
    if isinstance(value, dict):
        return {key: _rewrite_json(item) for key, item in value.items()}
    return _rewrite(value)


def rename_english_brand(apps, schema_editor):
    targets = (
        ("core", "SiteSettings"),
        ("pages", "HomePage"),
        ("pages", "AboutPage"),
        ("pages", "Certificate"),
        ("services", "Service"),
        ("news", "News"),
        ("team", "TeamMember"),
        ("team", "Case"),
    )
    for app_label, model_name in targets:
        model = apps.get_model(app_label, model_name)
        text_fields = []
        json_fields = []
        for field in model._meta.fields:
            if not field.name.endswith("_en"):
                continue
            if isinstance(field, models.JSONField):
                json_fields.append(field.name)
            elif isinstance(field, (models.CharField, models.TextField)):
                text_fields.append(field.name)
        for obj in model.objects.all():
            changed = False
            for field_name in text_fields:
                current = getattr(obj, field_name) or ""
                updated = _rewrite(current)
                if updated != current:
                    setattr(obj, field_name, updated)
                    changed = True
            for field_name in json_fields:
                current = getattr(obj, field_name)
                updated = _rewrite_json(current)
                if updated != current:
                    setattr(obj, field_name, updated)
                    changed = True
            if changed:
                obj.save()


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0009_site_name_en"),
        ("pages", "0007_site_name_en"),
        ("services", "0002_bilingual_en"),
        ("news", "0002_bilingual_en"),
        ("team", "0004_bilingual_en"),
    ]

    operations = [
        migrations.RunPython(rename_english_brand, migrations.RunPython.noop),
    ]
