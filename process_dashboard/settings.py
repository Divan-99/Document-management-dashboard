"""
Django settings for process_dashboard project.
"""

from pathlib import Path
import os

# ── Paths ─────────────────────────────────────────────────────────────────────

BASE_DIR = Path(__file__).resolve().parent.parent


# ── Security ──────────────────────────────────────────────────────────────────

# Change this to a long random string in production.
# Generate one with: python -c "import secrets; print(secrets.token_hex(50))"
SECRET_KEY = "django-insecure-change-this-before-going-to-production-abc123xyz"

# Set to False in production and configure ALLOWED_HOSTS properly
DEBUG = True

# Add your machine's IP or hostname here if accessing from other devices on the network
# e.g. ALLOWED_HOSTS = ["localhost", "127.0.0.1", "192.168.1.50"]
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "10.59.0.5", "dashboard.sa.iscar.com"]
CSRF_TRUSTED_ORIGINS = ["https://dashboard.sa.iscar.com", "https://label.sa.iscar.com", "https://isdoc.sa.iscar.com"]

# ── Applications ──────────────────────────────────────────────────────────────

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Dashboard app
    "dashboard",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "dashboard.middleware.BearerTokenMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "process_dashboard.urls"


# ── Templates ─────────────────────────────────────────────────────────────────

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],   # project-level templates folder
        "APP_DIRS": True,                   # also finds app-level templates/
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "process_dashboard.wsgi.application"


# ── Database ──────────────────────────────────────────────────────────────────
# SQLite is fine for this dashboard — it only stores Django admin/session data.
# Process state is managed in-memory by process_manager.py.

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# ── Password validation ───────────────────────────────────────────────────────

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# ── Internationalisation ──────────────────────────────────────────────────────

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Africa/Johannesburg"  # UTC+2
USE_I18N = True
USE_TZ = True


# ── Static files ──────────────────────────────────────────────────────────────

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"   # used by collectstatic in production

# Extra static file directories (none needed — APP_DIRS handles dashboard/static/)


# ── Default primary key ───────────────────────────────────────────────────────

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ── Login / auth ──────────────────────────────────────────────────────────────

LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/dashboard/"
LOGOUT_REDIRECT_URL = "/accounts/login/"


# ── Logging ───────────────────────────────────────────────────────────────────

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[{asctime}] {levelname} {name}: {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "dashboard": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}


# ── Session ───────────────────────────────────────────────────────────────────

SESSION_COOKIE_AGE = 86400 * 7   # 7 days

# ── Home Assistant API token ──────────────────────────────────────────────────
# Used by Home Assistant REST sensors to poll process status.
# Must match the Authorization header in HA configuration.yaml
DASHBOARD_API_TOKEN = "iscar-token-2026"
