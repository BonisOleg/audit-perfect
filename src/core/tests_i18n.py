from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django.utils import translation

from src.core.i18n import collapse_double_prefix, localize_path
from src.core.models import SiteSettings
from src.services.models import Service


class PathTests(TestCase):
    def test_localize_and_collapse(self):
        self.assertEqual(localize_path("/poslugy/viyskovyy-oblik/", "en"), "/en/poslugy/viyskovyy-oblik/")
        self.assertEqual(localize_path("/en/poslugy/viyskovyy-oblik/", "uk"), "/poslugy/viyskovyy-oblik/")
        self.assertEqual(localize_path("/", "en"), "/en/")
        self.assertEqual(localize_path("/en/", "uk"), "/")
        self.assertEqual(collapse_double_prefix("/en/en/poslugy/"), "/en/poslugy/")


class SwitcherTests(TestCase):
    def setUp(self):
        translation.activate("uk")
        self.client = Client()
        SiteSettings.load()
        Service.objects.create(
            title_uk="Військовий облік",
            title_en="Military registration",
            slug="viyskovyy-oblik",
            short_description_uk="тест",
            short_description_en="A test service",
            is_active=True,
        )

    def tearDown(self):
        translation.activate("uk")

    def test_switch_urls_on_home_and_service(self):
        home = self.client.get("/")
        self.assertContains(home, 'name="next" value="/en/"')
        self.assertContains(home, ">EN<")
        self.assertNotContains(home, ">UA<")
        page = self.client.get("/en/poslugy/viyskovyy-oblik/")
        self.assertEqual(page.status_code, 200)
        self.assertContains(page, 'name="next" value="/poslugy/viyskovyy-oblik/"')
        self.assertContains(page, ">UA<")
        self.assertNotContains(page, ">EN<")
        self.assertContains(page, "Military registration")
        self.assertContains(page, "Home")
        self.assertNotContains(page, "Аудиторська фірма")

    def test_post_cycle_returns_home(self):
        to_en = self.client.post("/i18n/setlang/", {"language": "en", "next": "/"})
        self.assertEqual(to_en.status_code, 302)
        self.assertEqual(to_en["Location"], "/en/")
        self.assertEqual(to_en.cookies["django_language"].value, "en")
        to_uk = self.client.post("/i18n/setlang/", {"language": "uk", "next": "/en/"})
        self.assertEqual(to_uk["Location"], "/")
        self.assertEqual(to_uk.cookies["django_language"].value, "uk")

    def test_double_prefix_collapses(self):
        response = self.client.get("/en/en/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/en/")

    def test_disabled_english_hides_button_and_redirects(self):
        site = SiteSettings.load()
        site.en_enabled = False
        site.save(update_fields=["en_enabled"])
        home = self.client.get("/")
        self.assertNotContains(home, 'name="language" value="en"')
        gone = self.client.get("/en/poslugy/viyskovyy-oblik/")
        self.assertEqual(gone.status_code, 302)
        self.assertEqual(gone["Location"], "/poslugy/viyskovyy-oblik/")

    @override_settings(LANGUAGE_CODE="uk")
    def test_empty_english_does_not_show_ukrainian_title(self):
        Service.objects.filter(slug="viyskovyy-oblik").update(title_en="")
        with translation.override("en"):
            service = Service.objects.get(slug="viyskovyy-oblik")
            self.assertEqual(service.title, "")
            self.assertNotEqual(service.title, service.title_uk)
