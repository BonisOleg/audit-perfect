from urllib.parse import urlsplit, urlunsplit

from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from src.core.i18n import localize_path
from src.news.models import News
from src.services.models import Service


class BilingualSitemapMixin:
    def get_urls(self, page=1, site=None, protocol=None):
        urls = super().get_urls(page=page, site=site, protocol=protocol)
        from src.core.models import SiteSettings

        if not SiteSettings.load().en_enabled:
            return urls
        extra = []
        for item in urls:
            parts = urlsplit(item["location"])
            en_path = localize_path(parts.path, "en")
            if en_path == parts.path:
                continue
            cloned = dict(item)
            cloned["location"] = urlunsplit((parts.scheme, parts.netloc, en_path, parts.query, ""))
            extra.append(cloned)
        return urls + extra


class StaticViewSitemap(BilingualSitemapMixin, Sitemap):
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


class ServiceSitemap(BilingualSitemapMixin, Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return Service.objects.filter(is_active=True)

    def location(self, obj):
        return obj.get_absolute_url()


class NewsSitemap(BilingualSitemapMixin, Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return News.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.published_at

    def location(self, obj):
        return obj.get_absolute_url()
