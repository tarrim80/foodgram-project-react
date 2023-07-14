import locale
import os
from pathlib import Path

from dotenv import load_dotenv

# __________________BASE______________ #

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY", "secret_key_public")

DEVELOPMENT_STATUS = os.getenv("DEVELOPMENT_STATUS", "PRODUCTION")
DEBUG = DEVELOPMENT_STATUS != "PRODUCTION"

ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "[*]").split(" ")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # libraries
    "colorfield",
    "django_filters",
    "rest_framework",
    "rest_framework.authtoken",
    "djoser",
    # apps
    "api.apps.ApiConfig",
    "recipes.apps.RecipesConfig",
    "users.apps.UsersConfig",
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

ROOT_URLCONF = "foodgram_backend.urls"

TEMPLATES_DIR = BASE_DIR / "templates"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATES_DIR],
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

WSGI_APPLICATION = "foodgram_backend.wsgi.application"


LANGUAGE_CODE = "ru-RU"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

locale.setlocale(locale.LC_ALL, "ru_RU.UTF-8")

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "collected_static")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

PAGE_SIZE = 6


# ______________DATABASES______________ #

DATABASES = {
    #     "default": {
    #         "ENGINE": "django.db.backends.sqlite3",
    #         "NAME": BASE_DIR / "db.sqlite3",
    #     }
    # }
    # if os.getenv("DEVELOPMENT_STATUS") == "DEVELOPMENT"
    # else {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", "db"),
        "USER": os.getenv("POSTGRES_USER", "user"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", ""),
        "HOST": os.getenv("POSTGRES_HOST", ""),
        "PORT": os.getenv("POSTGRES_PORT", 5432),
    }
}


# ______________AUTH_____________ #


AUTH_USER_MODEL = "users.User"

AUTH_PASSWORD_VALIDATORS = (
    [
        {
            "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa
        },
        {
            "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",  # noqa
        },
        {
            "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",  # noqa
        },
        {
            "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",  # noqa
        },
    ]
    if os.getenv("DEVELOPMENT_STATUS") == "PRODUCTION"
    else []
)


# ____________DRF____________ #

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
    ),
}


# _____________DJOSER_____________ #

DJOSER = {
    "LOGIN_FIELD": "email",
    "SERIALIZERS": {
        "user": "api.serializers.UserSerializer",
        "current_user": "api.serializers.UserSerializer",
        "user_create": "api.serializers.UserSerializer",
    },
    "HIDE_USERS": False,
    "PERMISSIONS": {
        "user": ("rest_framework.permissions.IsAuthenticated",),
        "user_list": ("rest_framework.permissions.AllowAny",),
    },
}


# _______________DEBUG_TOOLBAR________________ #

if DEBUG:
    INSTALLED_APPS += ("debug_toolbar",)

    MIDDLEWARE += ("debug_toolbar.middleware.DebugToolbarMiddleware",)

    INTERNAL_IPS = ("127.0.0.1",)


# _______________SHOPPING_LIST_____________________ #

SHOPPING_LIST_FILE_PARAMS = {
    "ADD_FONTS": [
        {
            "family": "Montserrat",
            "style": "",
            "fname": os.path.join(
                BASE_DIR, "media", "fonts", "Montserrat-Regular.ttf"
            ),
        },
        {
            "family": "Montserrat",
            "style": "I",
            "fname": os.path.join(
                BASE_DIR, "media", "fonts", "Montserrat-Italic.ttf"
            ),
        },
        {
            "family": "Montserrat",
            "style": "B",
            "fname": os.path.join(
                BASE_DIR, "media", "fonts", "Montserrat-Bold.ttf"
            ),
        },
        {
            "family": "Montserrat",
            "style": "BI",
            "fname": os.path.join(
                BASE_DIR, "media", "fonts", "Montserrat-BoldItalic.ttf"
            ),
        },
    ],
    "CELL_BORDER": False,
    "FILE_CREATE": {
        "orientation": "portrait",
        "unit": "mm",
        "format": "A4",
        "side_margin": 12,
        "top_margin": 5,
        "h_gap": 3,
        "v_gap": 2,
    },
    "HEADER": {
        "HEADER_TITLE_START": "Список покупок от",
        "HEADER_FONT": {"family": "montserrat", "style": "B", "size": 14},
    },
    "BASIC_PAGE": {
        "MAIN_FONT": {"family": "montserrat", "style": "", "size": 12},
        "PAGE_BREAK": {"auto": True, "margin": 23},
    },
    "FOOTER": {
        "LOGO_IMAGE": {
            "name": os.path.join(BASE_DIR, "media", "logo", "favicon.png"),
            "w": 12,
            "keep_aspect_ratio": True,
        },
        "FOOTER_Y": -20,
        "FOOTER_HEIGHT": 20,
        "FOOTER_TEXT_COLOR": 255,
        "FOOTER_FILL_COLOR": 0,
        "FOOTER_LABEL": "Продуктовый помощник",
        "FOOTER_FONT": {"family": "montserrat", "style": "", "size": 12},
        "FOOTER_MARGIN": 0,
    },
}

# __________________OTHER_CONSTANTS________________ #

MIN_COOKING_TIME = 1
MIN_INGREDIENT_AMOUNT = 1

MIGRATION_LIFETIME_SEC = 30
