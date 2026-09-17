from pathlib import Path
from tempfile import TemporaryDirectory

from django.test import Client, TestCase, override_settings
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

    def test_about_certificates(self):
        from django.core.files.uploadedfile import SimpleUploadedFile

        from src.pages.models import AboutPage, Certificate

        png = (
            b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01"
            b"\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00"
            b"\x00\x0cIDATx\x9cc\xf8\x0f\x00\x00\x01\x01\x00\x05"
            b"\x18\xd8N\x00\x00\x00\x00IEND\xaeB`\x82"
        )
        page = AboutPage.load()
        with TemporaryDirectory() as tmp:
            with override_settings(MEDIA_ROOT=Path(tmp)):
                Certificate.objects.create(
                    about=page,
                    title="Диплом ACCA (DipIFR)",
                    image=SimpleUploadedFile("acca.png", png, content_type="image/png"),
                    sort_order=1,
                    is_active=True,
                )
                r = self.client.get(reverse("pages:about"))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Диплом ACCA (DipIFR)")
        self.assertContains(r, "data-certs-open")

    def test_criticality_redirect(self):
        r = self.client.get("/poslugy/pryznachennya-krytychnosti/")
        self.assertEqual(r.status_code, 301)
        self.assertEqual(r["Location"], "/poslugy/viyskovyy-oblik/")
