from django.db import migrations


def _text(blocks, page, key, fallback=""):
    block = blocks.get((page, key))
    if not block:
        return fallback
    return (block.body or "").strip() or fallback


def _title(blocks, page, key, fallback=""):
    block = blocks.get((page, key))
    if not block:
        return fallback
    return (block.title or "").strip() or fallback


def copy_blocks(apps, schema_editor):
    SiteBlock = apps.get_model("core", "SiteBlock")
    HomePage = apps.get_model("pages", "HomePage")
    AboutPage = apps.get_model("pages", "AboutPage")
    blocks = {(item.page, item.key): item for item in SiteBlock.objects.all()}

    home, _ = HomePage.objects.get_or_create(pk=1)
    home.hero_title = _text(blocks, "home", "hero_title", home.hero_title)
    home.hero_lead = _text(blocks, "home", "hero_lead", home.hero_lead)
    home.why_1_title = _title(blocks, "home", "why_1", home.why_1_title)
    home.why_1_body = _text(blocks, "home", "why_1", home.why_1_body)
    home.why_2_title = _title(blocks, "home", "why_2", home.why_2_title)
    home.why_2_body = _text(blocks, "home", "why_2", home.why_2_body)
    home.why_3_title = _title(blocks, "home", "why_3", home.why_3_title)
    home.why_3_body = _text(blocks, "home", "why_3", home.why_3_body)
    home.save()

    about, _ = AboutPage.objects.get_or_create(pk=1)
    about.lead = _text(blocks, "about", "about_lead", about.lead)
    about.story = _text(blocks, "about", "about_story", about.story)
    about.stat_1_value = _title(blocks, "about", "stat_1", about.stat_1_value)
    about.stat_1_label = _text(blocks, "about", "stat_1", about.stat_1_label)
    about.stat_2_value = _title(blocks, "about", "stat_2", about.stat_2_value)
    about.stat_2_label = _text(blocks, "about", "stat_2", about.stat_2_label)
    about.stat_3_value = _title(blocks, "about", "stat_3", about.stat_3_value)
    about.stat_3_label = _text(blocks, "about", "stat_3", about.stat_3_label)
    about.stat_4_value = _title(blocks, "about", "stat_4", about.stat_4_value)
    about.stat_4_label = _text(blocks, "about", "stat_4", about.stat_4_label)
    about.save()


class Migration(migrations.Migration):
    dependencies = [
        ("pages", "0001_initial"),
        ("core", "0003_sitesettings_page_seo_and_block_labels"),
    ]

    operations = [
        migrations.RunPython(copy_blocks, migrations.RunPython.noop),
    ]
