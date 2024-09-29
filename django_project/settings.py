from dotenv import load_dotenv
import pathlib
from datetime import date
import os

load_dotenv()
today = date.today()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = pathlib.Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(os.environ.get("DEVELOP")))

if not bool(int(os.environ.get("DEVELOP"))):
    ALLOWED_HOSTS = [
        "localhost",
        "apps.iubase.com",
        "159.203.11.18",
    ]
else:
    ALLOWED_HOSTS = [
        "localhost",
        "127.0.0.1",
    ]


INSTALLED_APPS = [
    "django_project",
    "index",
    "live_game_blog",
    "player_tracking",
    "accounts",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "django_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "django_project/templates"],
        "APP_DIRS": True,
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

WSGI_APPLICATION = "django_project.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "iubase",
        "USER": "iubase",
        "PASSWORD": os.environ.get("DB_PASSWORD"),
        "HOST": "localhost",
        "PORT": "5432",
    }
}

if DEBUG:
    log_level = "DEBUG"
else:
    log_level = "WARNING"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "level": log_level,
            "class": "logging.FileHandler",
            "filename": f"{BASE_DIR}/logs/{today.year}_{today.strftime("%m")}_logging.log",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": log_level,
            "propagate": True,
        },
    },
}


# Password validation

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

# Registration

LOGIN_REDIRECT_URL = "index"

LOGOUT_REDIRECT_URL = "index"


# Internationalization

LANGUAGE_CODE = "en-us"

TIME_ZONE = "America/Indiana/Indianapolis"

USE_I18N = True

USE_TZ = True


STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "accounts.CustomUser"

if not bool(int(os.environ.get("DEVELOP"))):
    # added due to security warnings
    CSRF_COOKIE_SECURE = True

    SECURE_HSTS_SECONDS = 9999

    SECURE_SSL_REDIRECT = True

    SECURE_HSTS_INCLUDE_SUBDOMAINS = True

    SECURE_HSTS_PRELOAD = True

    SESSION_COOKIE_SECURE = True

    STATIC_ROOT = os.path.join(BASE_DIR, "django_project/static/")


project_version = (
    "0.1.28"  # ALL Style enhancements ATP 2024-09-29
)
os.environ.setdefault("PROJECT_VERSION", project_version)
