from django.test import Client, TestCase
from django.urls import reverse

from src.services.models import Service


class SmokeTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Service.objects.create(
            title="Військовий облік",
            slug="viyskovyy-oblik",
            short_description="test",
            sort_order=1,
            is_active=True,
            composition=[{"title": "A", "text": "B"}],
        )

    def setUp(self):
        self.client = Client()

    def test_home(self):
        r = self.client.get(reverse("home"))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "corporate-website-v2")
        self.assertContains(r, "nofollow")

    def test_about_footer_no_agency_link(self):
        r = self.client.get(reverse("pages:about"))
        self.assertEqual(r.status_code, 200)
        self.assertNotContains(r, "corporate-website-v2")

    def test_criticality_redirect(self):
        r = self.client.get("/poslugy/pryznachennya-krytychnosti/")
        self.assertEqual(r.status_code, 301)
        self.assertEqual(r["Location"], "/poslugy/viyskovyy-oblik/")
