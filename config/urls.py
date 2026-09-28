from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.http import HttpResponse
from django.urls import include, path

from src.core.sitemaps import NewsSitemap, ServiceSitemap, StaticViewSitemap
from src.core.views import healthz
from src.core.views_i18n import set_language
from src.pages.views import HomeView

sitemaps = {
    "static": StaticViewSitemap,
    "services": ServiceSitemap,
    "news": NewsSitemap,
}


def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        f"Sitemap: {settings.SITE_URL}/sitemap.xml",
        "",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("tinymce/", include("tinymce.urls")),
    path("i18n/setlang/", set_language, name="set_language"),
    path("healthz/", healthz, name="healthz"),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
    path("robots.txt", robots_txt, name="robots"),
]

urlpatterns += i18n_patterns(
    path("", HomeView.as_view(), name="home"),
    path("", include("src.pages.urls")),
    path("poslugy/", include("src.services.urls")),
    path("novyny/", include("src.news.urls")),
    prefix_default_language=False,
)

handler404 = "src.pages.views_errors.page_not_found"

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
