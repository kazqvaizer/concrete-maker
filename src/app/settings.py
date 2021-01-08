from datetime import timedelta

import environ
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

settings_dir = environ.Path(__file__) - 1  # Cut off current file name
root = environ.Path(__file__) - 3  # Directory where "src" sub-directory is located
env = environ.Env(
    DEBUG=(bool, False),
)

ENV_FILE = env("ENV_FILE", default=None) or ".env"

environ.Env.read_env(env_file=settings_dir(ENV_FILE))  # reading .env file

SITE_ROOT = root()

DEBUG = env("DEBUG")

CI = env("CI", cast=bool, default=False)

SECRET_KEY = env("SECRET_KEY")

TIME_ZONE = env("TIME_ZONE")

SENTRY_DSN = env("SENTRY_DSN", default=None)

if SENTRY_DSN is not None:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        traces_sample_rate=1.0,
        send_default_pii=True,
    )

ALLOWED_HOSTS = [
    "concrete.kazqvaizer.xyz",
    "localhost",
    "127.0.0.1",
]

STATIC_URL = "/static/"
STATIC_ROOT = "/static"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": env("DATABASE_NAME"),
    }
}

# Application definition

INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 3-rd party
    "behaviors.apps.BehaviorsConfig",
    "corsheaders",
    "rest_framework",
    "rest_framework.authtoken",
    # Current project
    "app.apps.ConcreteMakerAppConfig",
    "lab.apps.LabConfig",
    "production.apps.ProductionConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "app.middleware.JWTAuthMiddleware",
    "app.middleware.TokenAuthMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "app.urls"
WSGI_APPLICATION = "app.wsgi.application"

LANGUAGE_CODE = "ru"
USE_L10N = True
USE_i18N = True
USE_TZ = True
LOCALE_PATHS = ["_locale"]


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "DEBUG",  # Changed from default `INFO` level
            "class": "logging.StreamHandler",
        },
    },
}

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.DjangoModelPermissions",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=3),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=14),
    "AUTH_HEADER_TYPES": ("JWT",),
}

HEALTH_CHECKS_ERROR_CODE = 503
HEALTH_CHECKS = {
    "db": "django_healthchecks.contrib.check_database",
}
