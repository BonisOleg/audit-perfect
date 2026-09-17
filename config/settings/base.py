from pathlib import Path

from csp.constants import NONCE, SELF
from decouple import Csv, config
from django.urls import reverse_lazy

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = config("SECRET_KEY")

DEBUG = False

ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="", cast=Csv())

SITE_URL = config("SITE_URL", default="https://example.com").rstrip("/")

GA4_MEASUREMENT_ID = config("GA4_MEASUREMENT_ID", default="")

INSTALLED_APPS = [
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "django_htmx",
    "csp",
    "tinymce",
    "src.core",
    "src.pages",
    "src.services",
    "src.news",
    "src.team",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
    "csp.middleware.CSPMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "src.core.context_processors.site_globals",
                "csp.context_processors.nonce",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "uk"
TIME_ZONE = "Europe/Kyiv"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = []
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

APPEND_SLASH = True

UNFOLD = {
    "SITE_TITLE": "Аудит-Перфект",
    "SITE_HEADER": "Аудит-Перфект",
    "SITE_SYMBOL": "account_balance",
    "SHOW_HISTORY": True,
    "SIDEBAR": {
        "show_search": True,
        "navigation": [
            {
                "title": "Контент",
                "items": [
                    {
                        "title": "Налаштування сайту",
                        "icon": "settings",
                        "link": reverse_lazy("admin:core_sitesettings_changelist"),
                    },
                    {
                        "title": "CMS-блоки",
                        "icon": "view_module",
                        "link": reverse_lazy("admin:core_siteblock_changelist"),
                    },
                    {
                        "title": "Послуги",
                        "icon": "work",
                        "link": reverse_lazy("admin:services_service_changelist"),
                    },
                    {
                        "title": "Новини",
                        "icon": "newspaper",
                        "link": reverse_lazy("admin:news_news_changelist"),
                    },
                    {
                        "title": "Команда",
                        "icon": "groups",
                        "link": reverse_lazy("admin:team_teammember_changelist"),
                    },
                    {
                        "title": "Кейси",
                        "icon": "folder",
                        "link": reverse_lazy("admin:team_case_changelist"),
                    },
                ],
            },
        ],
    },
}

CONTENT_SECURITY_POLICY = {
    "DIRECTIVES": {
        "default-src": [SELF],
        "script-src": [SELF, NONCE, "https://www.googletagmanager.com"],
        "style-src": [SELF, "https://fonts.googleapis.com"],
        "font-src": [SELF, "https://fonts.gstatic.com", "data:"],
        "img-src": [SELF, "data:", "https:"],
        "connect-src": [
            SELF,
            "https://www.google-analytics.com",
            "https://www.googletagmanager.com",
        ],
        "frame-src": [
            SELF,
            "https://www.google.com",
            "https://www.openstreetmap.org",
        ],
        "frame-ancestors": [SELF],
    }
}

TINYMCE_DEFAULT_CONFIG = {
    "height": 360,
    "menubar": False,
    "plugins": "lists link",
    "toolbar": "undo redo | bold italic | bullist numlist | link | removeformat",
    "branding": False,
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {"handlers": ["console"], "level": "WARNING"},
    "loggers": {
        "src": {"handlers": ["console"], "level": "INFO", "propagate": False},
        "django": {"handlers": ["console"], "level": "WARNING", "propagate": False},
    },
}
