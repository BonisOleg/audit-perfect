from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from src.news.models import News
from src.services.models import Service


class StaticViewSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return [
            "home",
            "pages:about",
            "services:list",
            "news:list",
            "pages:contacts",
            "pages:policy",
        ]

    def location(self, item):
        return reverse(item)


class ServiceSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return Service.objects.filter(is_active=True)

    def location(self, obj):
        return obj.get_absolute_url()


class NewsSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return News.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.published_at

    def location(self, obj):
        return obj.get_absolute_url()
