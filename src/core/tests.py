from django.contrib.auth.models import User
from django.test import Client, TestCase

from src.core.models import SiteSettings
from src.core.richtext import render_cms_inline, render_cms_text
from src.services.admin import _lines_to_composition


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
