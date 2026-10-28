import os
from pathlib import Path

import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = os.environ.get("DEBUG", "True").lower() == "true"

# Use a private key from the environment in production.
SECRET_KEY = os.environ.get("SECRET_KEY")
if not SECRET_KEY:
    if DEBUG:
        SECRET_KEY = "django-insecure-local-development-only-change-this"
    else:
        from django.core.exceptions import ImproperlyConfigured
        raise ImproperlyConfigured(
            "Set the SECRET_KEY environment variable before running with DEBUG=False."
        )

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
render_hostname = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if render_hostname:
    ALLOWED_HOSTS.append(render_hostname)

extra_hosts = os.environ.get("ALLOWED_HOSTS", "")
if extra_hosts:
    ALLOWED_HOSTS.extend(
        host.strip() for host in extra_hosts.split(",") if host.strip()
    )

CLOUDINARY_ENABLED = bool(os.environ.get("CLOUDINARY_URL", "").strip())

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "marketplace",
]

# Enable cloud media storage only when CLOUDINARY_URL is configured on Render.
if CLOUDINARY_ENABLED:
    INSTALLED_APPS = ["cloudinary_storage", "cloudinary", *INSTALLED_APPS]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "marketplace.context_processors.cart_summary",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# Render supplies DATABASE_URL for PostgreSQL. Locally, use SQLite by default.
database_url = os.environ.get("DATABASE_URL")
if database_url:
    DATABASES = {
        "default": dj_database_url.parse(
            database_url,
            conn_max_age=600,
            ssl_require=not DEBUG,
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-in"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

STORAGES = {
    "default": {
        "BACKEND": (
            "cloudinary_storage.storage.MediaCloudinaryStorage"
            if CLOUDINARY_ENABLED
            else "django.core.files.storage.FileSystemStorage"
        ),
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}
# Compatibility for django-cloudinary-storage's collectstatic command.
STATICFILES_STORAGE = (
    "whitenoise.storage.CompressedManifestStaticFilesStorage"
    if not DEBUG
    else "django.contrib.staticfiles.storage.StaticFilesStorage"
)

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"

CSRF_TRUSTED_ORIGINS = []
if render_hostname:
    CSRF_TRUSTED_ORIGINS.append(f"https://{render_hostname}")

extra_csrf_origins = os.environ.get("CSRF_TRUSTED_ORIGINS", "")
if extra_csrf_origins:
    CSRF_TRUSTED_ORIGINS.extend(
        origin.strip()
        for origin in extra_csrf_origins.split(",")
        if origin.strip()
    )

if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
