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
        self.assertContains(r, "images/hero.webp")
        self.assertNotContains(r, "<video")

    def test_home_admin_shows_multiple_slide_uploads(self):
        from django.contrib.auth.models import User

        from src.pages.models import HomePage

        User.objects.create_superuser("admin", "admin@localhost", "admin12345")
        self.client.login(username="admin", password="admin12345")
        HomePage.load()
        response = self.client.get(reverse("admin:pages_homepage_change", args=[1]))
        self.assertEqual(response.status_code, 200)
        html = response.content.decode()
        self.assertLess(
            html.find("hero_slides-0-image"),
            html.find("id_hero_title"),
        )
        for index in range(3):
            self.assertContains(response, f'name="hero_slides-{index}-image"')
        self.assertContains(response, "Фото слайдера")

    def test_home_hero_modes(self):
        from django.core.files.uploadedfile import SimpleUploadedFile

        from src.pages.models import HeroSlide, HomePage

        png = (
            b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01"
            b"\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00"
            b"\x00\x0cIDATx\x9cc\xf8\x0f\x00\x00\x01\x01\x00\x05"
            b"\x18\xd8N\x00\x00\x00\x00IEND\xaeB`\x82"
        )
        page = HomePage.load()
        with TemporaryDirectory() as tmp:
            with override_settings(MEDIA_ROOT=Path(tmp)):
                page.hero_mode = HomePage.HeroMode.IMAGE
                page.hero_image = SimpleUploadedFile("banner.png", png, content_type="image/png")
                page.save()
                image_response = self.client.get(reverse("home"))

                page.hero_image = ""
                page.hero_mode = HomePage.HeroMode.SLIDER
                page.save()
                HeroSlide.objects.create(
                    home=page,
                    image=SimpleUploadedFile("a.png", png, content_type="image/png"),
                    sort_order=1,
                    is_active=True,
                )
                HeroSlide.objects.create(
                    home=page,
                    image=SimpleUploadedFile("b.png", png, content_type="image/png"),
                    sort_order=2,
                    is_active=False,
                )
                one_slide = self.client.get(reverse("home"))
                HeroSlide.objects.create(
                    home=page,
                    image=SimpleUploadedFile("c.png", png, content_type="image/png"),
                    sort_order=3,
                    is_active=True,
                )
                slider = self.client.get(reverse("home"))

                page.hero_mode = HomePage.HeroMode.VIDEO
                page.hero_video = SimpleUploadedFile("loop.mp4", b"fake-mp4", content_type="video/mp4")
                page.hero_poster = SimpleUploadedFile("poster.png", png, content_type="image/png")
                page.save()
                video = self.client.get(reverse("home"))

        self.assertContains(image_response, "/media/hero/banner")
        self.assertNotContains(image_response, "images/hero.webp")
        self.assertContains(one_slide, "/media/hero/slides/a")
        self.assertNotContains(one_slide, "data-hero-slide")
        self.assertContains(slider, 'data-hero-kind="slider"')
        self.assertContains(slider, "data-hero-slide", count=2)
        self.assertNotContains(slider, "/media/hero/slides/b")
        self.assertContains(video, "playsinline")
        self.assertContains(video, "muted")
        self.assertContains(video, "/media/hero/video/loop")
        self.assertContains(video, "/media/hero/poster/poster")

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

    def test_about_team_photo_upload_and_inactive(self):
        from django.core.files.uploadedfile import SimpleUploadedFile

        from src.pages.models import AboutPage
        from src.team.models import TeamMember

        png = (
            b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01"
            b"\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00"
            b"\x00\x0cIDATx\x9cc\xf8\x0f\x00\x00\x01\x01\x00\x05"
            b"\x18\xd8N\x00\x00\x00\x00IEND\xaeB`\x82"
        )
        page = AboutPage.load()
        with TemporaryDirectory() as tmp:
            with override_settings(MEDIA_ROOT=Path(tmp)):
                TeamMember.objects.create(
                    about=page,
                    name="Наталія Єсієва",
                    role="Директор",
                    photo=SimpleUploadedFile("yesieva.png", png, content_type="image/png"),
                    sort_order=1,
                    is_active=True,
                )
                TeamMember.objects.create(
                    about=page,
                    name="Прихована",
                    role="Не на сайті",
                    sort_order=2,
                    is_active=False,
                )
                r = self.client.get(reverse("pages:about"))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Наталія Єсієва")
        self.assertContains(r, "/media/team/yesieva")
        self.assertNotContains(r, "Прихована")

    def test_criticality_redirect(self):
        r = self.client.get("/poslugy/pryznachennya-krytychnosti/")
        self.assertEqual(r.status_code, 301)
        self.assertEqual(r["Location"], "/poslugy/viyskovyy-oblik/")
