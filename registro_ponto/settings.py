from pathlib import Path
import dj_database_url
import os
from collections import OrderedDict

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

IS_HEROKU_APP = "DYNO" in os.environ and not "CI" in os.environ
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
APP_PORT = os.environ.get("APP_PORT", 8000)
# SECURITY WARNING: don't run with debug turned on in production!
if not IS_HEROKU_APP:
    DEBUG = True


# On Heroku, it's safe to use a wildcard for `ALLOWED_HOSTS``, since the Heroku router performs
# validation of the Host header in the incoming HTTP request. On other platforms you may need to
# list the expected hostnames explicitly in production to prevent HTTP Host header attacks. See:
# https://docs.djangoproject.com/en/5.1/ref/settings/#std-setting-ALLOWED_HOSTS
if IS_HEROKU_APP:
    ALLOWED_HOSTS = ["*"]
else:
    ALLOWED_HOSTS = [".localhost", "127.0.0.1", "[::1]", "0.0.0.0"]
    CORS_ORIGIN_WHITELIST = [
        f"http://localhost:{APP_PORT}",
    ]
    CSRF_TRUSTED_ORIGINS = [
        f"http://localhost:{APP_PORT}",
    ]

# Application definition

THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework_nested",
    "crispy_forms",
    "crispy_bootstrap5",
    "whitenoise.runserver_nostatic",
    "django_extensions",
]

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

INTERNAL_APPS = [
    "core",
    "apps.colaboradores",
    "apps.credenciais",
    "apps.public",
]

INSTALLED_APPS = THIRD_PARTY_APPS + DJANGO_APPS + INTERNAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django_session_timeout.middleware.SessionTimeoutMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "core.middleware.LoginRequiredMiddleware",
]

# Crispy forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Login
LOGIN_URL = "auth_web:login"
LOGIN_REDIRECT_URL = "internal_home"

# Login Middleware
PUBLIC_URL_NAMES = [
    # Public
    "public_home",
    "public_web:orcamento",
    "public_web:orcamento_save",
    # Autenticação
    "auth_web:login",
    "auth_api:auth-login",
]

# Expiration time for sessions
SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True
SESSION_EXPIRE_SECONDS = 1800  # 30min
SESSION_TIMEOUT_REDIRECT = LOGIN_URL

ROOT_URLCONF = "registro_ponto.urls"

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
                "core.context_processors.default_context",
                "core.context_processors.menu_options",
                "core.context_processors.env_vars",
            ],
        },
    },
]

TEMPLATES_PLUGINS = OrderedDict(
    {
        "apexcharts": {
            "js": ["core/libs/apexcharts/apexcharts.min.js"],
        },
        "awesomplete": {
            "css": ["core/libs/awesomplete/awesomplete.css"],
            "js": ["core/libs/awesomplete/awesomplete.min.js"],
        },
        "choices.js": {
            "css": ["core/libs/choices.js/choices.min.css"],
            "js": ["core/libs/choices.js/choices.min.js"],
        },
        "bootstrap_datetimepicker": {
            "js": ["core/libs/datepicker/bootstrap-datetimepicker.min.js"],
        },
        "bootstrap_slider": {
            "css": ["core/libs/bootstrap-slider/bootstrap-slider.min.css"],
            "js": ["core/libs/bootstrap-slider/bootstrap-slider.min.js"],
        },
        "decimal": {
            "js": ["core/libs/decimal/decimal.min.js"],
        },
        "flatpickr": {
            "css": [
                "core/libs/flatpickr/flatpickr.min.css",
                "core/libs/flatpickr/plugins/monthSelect/style.css",
            ],
            "js": [
                "core/libs/flatpickr/flatpickr.min.js",
                "core/libs/flatpickr/plugins/monthSelect/index.js",
                "core/libs/flatpickr/l10n/pt.js",
            ],
        },
        "loading.io": {
            "css": ["core/libs/loading.io/loading.io.min.css"],
        },
        "sheetjs": {
            "js": ["core/libs/sheetjs/xlsx.full.min.js"],
        },
        "picojs": {
            "js": [
                "core/libs/picojs/pico.min.js",
                "core/libs/picojs/lploc.min.js",
                "core/libs/picojs/camera.min.js",
                "core/libs/picojs/init.min.js",
            ],
        },
        "sortable": {
            "js": ["core/libs/sortable/sortable.min.js"],
        },
        "vanilla_masker": {
            "js": ["core/libs/vanilla-masker/vanilla-masker.min.js"],
        },
        "tabulator": {
            "css": [
                "core/libs/tabulator/css/tabulator.min.css",
                "core/libs/tabulator/css/tabulator_bootstrap5.min.css",
                "core/libs/tabulator/css/tabulator_custom.css",
            ],
            "js": [
                "core/libs/tabulator/js/tabulator.min.js",
                "core/libs/tabulator/js/tabulator_defaults.js",
            ],
        },
        "tom-select": {
            "css": ["core/libs/tom-select/tom-select.min.css"],
            "js": ["core/libs/tom-select/tom-select.min.js"],
        },
    }
)

WSGI_APPLICATION = "registro_ponto.wsgi.application"

# REST_FRAMEWORK
DEFAULT_RENDERER_CLASSES = ("rest_framework.renderers.JSONRenderer",)

if not IS_HEROKU_APP:
    DEFAULT_RENDERER_CLASSES = DEFAULT_RENDERER_CLASSES + (
        "rest_framework.renderers.BrowsableAPIRenderer",
    )

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_RENDERER_CLASSES": DEFAULT_RENDERER_CLASSES,
    "EXCEPTION_HANDLER": "core.exceptions.custom_exception_handler",
}


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

if IS_HEROKU_APP:
    DATABASES = {
        "default": dj_database_url.config(
            env="DATABASE_URL",
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=True,
        ),
    }
else:
    DATABASES = {
        "default": dj_database_url.config(
            env="DATABASE_URL",
            conn_max_age=600,
            conn_health_checks=True,
        ),
    }


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "pt-br"

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/


STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": True,
        },
    },
}
