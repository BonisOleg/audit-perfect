from django.contrib.auth.models import User
from django.test import Client, TestCase

from src.core.models import SiteSettings
from src.core.richtext import render_cms_inline, render_cms_text
from src.services.admin import _lines_to_composition


class UploadedImageWebpTests(TestCase):
    def test_png_upload_is_stored_as_webp(self):
        import io
        from pathlib import Path
        from tempfile import TemporaryDirectory

        from django.core.files.uploadedfile import SimpleUploadedFile
        from django.test import override_settings
        from PIL import Image

        from src.pages.models import HomePage

        buffer = io.BytesIO()
        Image.new("RGB", (2, 2), (200, 10, 10)).save(buffer, format="PNG")
        png = buffer.getvalue()
        page = HomePage.load()
        with TemporaryDirectory() as tmp:
            with override_settings(MEDIA_ROOT=Path(tmp)):
                page.hero_image = SimpleUploadedFile("banner.png", png, content_type="image/png")
                page.save()
                stored = page.hero_image.name
                payload = page.hero_image.read()
                page.hero_title = page.hero_title
                page.save()
                page.refresh_from_db()
        self.assertTrue(stored.endswith(".webp"))
        self.assertTrue(payload.startswith(b"RIFF"))
        self.assertIn(b"WEBP", payload[:16])
        self.assertEqual(page.hero_image.name, stored)

    def test_webp_upload_is_kept(self):
        import io
        from tempfile import TemporaryDirectory
        from pathlib import Path

        from django.core.files.uploadedfile import SimpleUploadedFile
        from django.test import override_settings
        from PIL import Image

        from src.pages.models import HomePage

        buffer = io.BytesIO()
        Image.new("RGB", (2, 2), (10, 20, 30)).save(buffer, format="WEBP", quality=80)
        original = buffer.getvalue()
        page = HomePage.load()
        with TemporaryDirectory() as tmp:
            with override_settings(MEDIA_ROOT=Path(tmp)):
                page.hero_image = SimpleUploadedFile(
                    "banner.webp", original, content_type="image/webp"
                )
                page.save()
                payload = page.hero_image.read()
        self.assertTrue(page.hero_image.name.endswith("banner.webp"))
        self.assertEqual(payload, original)


class HealthzTests(TestCase):
    def test_healthz(self):
        response = self.client.get("/healthz/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"ok")


class AdminFunctionalTests(TestCase):
    def setUp(self):
        self.client = Client()
        User.objects.create_superuser("admin", "admin@localhost", "admin12345")

    def test_admin_login_has_no_csp(self):
        response = self.client.get("/admin/login/")
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("Content-Security-Policy", response.headers)

    def test_user_changelist_uses_unfold(self):
        self.client.login(username="admin", password="admin12345")
        response = self.client.get("/admin/auth/user/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "x-model")


class ThemeColorTests(TestCase):
    def test_derived_colors_follow_the_five_bases(self):
        from src.core.palette import build_theme_css

        css = build_theme_css("#ec423c", "#002fa7", "#141824", "#ffffff", "#f7f6f3")
        self.assertIn("--red:#ec423c;", css)
        self.assertIn("--blue:#002fa7;", css)
        self.assertIn("--ink:#141824;", css)
        self.assertIn("--bg:#ffffff;", css)
        self.assertIn("--wash:#f7f6f3;", css)
        self.assertIn("--btn:#141824;", css)
        self.assertIn("--on-btn:#ffffff;", css)
        self.assertIn("--red-deep:#c63732;", css)
        self.assertIn("--hero:#0b0d14;", css)
        self.assertNotIn("<", css)

    def test_home_uses_saved_palette(self):
        site = SiteSettings.load()
        site.color_red = "#112233"
        site.save()
        response = self.client.get("/")
        self.assertContains(response, "--red:#112233;")
        policy = response.headers["Content-Security-Policy"]
        nonce = policy.split("'nonce-", 1)[1].split("'", 1)[0]
        self.assertTrue(nonce)
        self.assertContains(response, f'nonce="{nonce}"')

    def test_admin_color_fields_are_pickers(self):
        User.objects.create_superuser("admin", "admin@localhost", "admin12345")
        self.client.login(username="admin", password="admin12345")
        SiteSettings.load()
        response = self.client.get("/admin/core/sitesettings/1/change/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'type="color"', count=5)


class ThemeFontTests(TestCase):
    def test_unknown_slug_falls_back_to_defaults(self):
        from src.core.fonts import font_stack, google_fonts_href

        self.assertEqual(
            font_stack("comic-sans", "onest"),
            '"Onest","Helvetica Neue",sans-serif',
        )
        href = google_fonts_href("nope", "also-nope")
        self.assertIn("family=Onest:wght@400;500;600;700", href)
        self.assertIn("family=Manrope:wght@400;500;600;700", href)
        self.assertNotIn("family=Inter", href)

    def test_same_family_is_requested_once(self):
        from src.core.fonts import google_fonts_href

        href = google_fonts_href("inter", "inter")
        self.assertEqual(href.count("family="), 1)
        self.assertIn("family=Inter:wght@400;500;600;700", href)
        spaced = google_fonts_href("source-sans-3", "manrope")
        self.assertIn("family=Source+Sans+3:wght@400;500;600;700", spaced)

    def test_home_uses_selected_fonts(self):
        site = SiteSettings.load()
        site.font_display = "inter"
        site.font_body = "source-sans-3"
        site.save()
        response = self.client.get("/")
        self.assertContains(response, '--ff-display:"Inter","Helvetica Neue",sans-serif;')
        self.assertContains(response, '--ff-body:"Source Sans 3","Helvetica Neue",sans-serif;')
        self.assertContains(
            response,
            "family=Inter:wght@400;500;600;700&amp;family=Source+Sans+3:wght@400;500;600;700",
        )
        self.assertNotContains(response, "family=Onest:")

    def test_admin_lists_ten_fonts(self):
        User.objects.create_superuser("admin", "admin@localhost", "admin12345")
        self.client.login(username="admin", password="admin12345")
        SiteSettings.load()
        response = self.client.get("/admin/core/sitesettings/1/change/")
        self.assertEqual(response.status_code, 200)
        for label in (
            "Onest",
            "Manrope",
            "Inter",
            "Source Sans 3",
            "IBM Plex Sans",
            "Nunito Sans",
            "Noto Sans",
            "Rubik",
            "Fira Sans",
            "Wix Madefor Text",
        ):
            self.assertContains(response, f">{label}<")


class SiteSettingsMetaTests(TestCase):
    def test_meta_for_uses_page_then_default(self):
        site = SiteSettings.load()
        site.home_meta_title = "Головна кастом"
        site.home_meta_description = ""
        site.save()
        title, description = site.meta_for("home")
        self.assertEqual(title, "Головна кастом")
        self.assertEqual(description, site.default_meta_description)


class CompositionAndRichtextTests(TestCase):
    def test_lines_to_composition(self):
        items = _lines_to_composition("Аудит | текст\nДругий")
        self.assertEqual(
            items,
            [{"title": "Аудит", "text": "текст"}, {"title": "Другий", "text": ""}],
        )

    def test_render_cms_text_plain_and_html(self):
        self.assertIn("<p>", render_cms_text("рядок"))
        self.assertEqual(str(render_cms_text("<p>готово</p>")), "<p>готово</p>")

    def test_render_cms_inline_unwraps_single_p(self):
        self.assertEqual(str(render_cms_inline("<p>готово</p>")), "готово")
