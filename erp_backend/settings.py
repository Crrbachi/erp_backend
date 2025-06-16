"""
Django settings for erp_backend project
======================================

– Django 5.2
– Preparado para producción (DEBUG=False) y desarrollo local
– Variables sensibles se cargan desde .env o desde variables
  de entorno (en Cloud Run / GitHub Actions)
"""

from pathlib import Path
import os, json, dotenv

# ──────────────────── Rutas básicas ────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent

# ────────────── Cargar variables del entorno ───────────
#  1. En local lee el fichero .env (si existe)
#  2. En Cloud Run simplemente usa las env-vars ya definidas en el servicio
dotenv.load_dotenv(BASE_DIR / ".env")

# ────────────────── Seguridad global ───────────────────
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Nunca publiques este valor en Git: usa SECRET_KEY en .env o variable de entorno
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-solo-local")

# ALLOWED_HOSTS en JSON para permitir varios dominios fácilmente
#   Ej.: '["erp-api-xxxxx.run.app", "api.midominio.com"]'
ALLOWED_HOSTS = json.loads(os.getenv("ALLOWED_HOSTS_JSON", '["localhost"]'))

# ───────────────── App y middleware ────────────────────
INSTALLED_APPS = [
    # Django core
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Terceros
    "rest_framework",              # Bloque 2
    "corsheaders",                 # Bloque 2
    # Propias (añadiremos más después)
    # "core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",        #  CORS siempre primero
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "erp_backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "erp_backend.wsgi.application"

# ───────────────────── Base de datos ───────────────────
#  Local: usa .env  ─  Cloud Run: variables definidas en el servicio
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME", "erp"),
        "USER": os.getenv("DB_USER", "erpadmin"),
        "PASSWORD": os.getenv("DB_PASS", ""),
        "HOST": os.getenv("DB_HOST", "localhost"),   # /cloudsql/... en Cloud Run
        "PORT": os.getenv("DB_PORT", "5432"),
    }
}

# ─────────────── Password validators (por defecto) ─────
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ─────────────── Internacionalización ────────────────
LANGUAGE_CODE = "es-es"
TIME_ZONE = "Europe/Madrid"
USE_I18N = True
USE_TZ = True

# ───────────────── Archivos estáticos ─────────────────
STATIC_URL  = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"     # se llenará con collectstatic

# ─────────────  Clave prim. por defecto ───────────────
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ─────────────  Django REST Framework base ────────────
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",   # cambiar a JWT en Bloque 2
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.AllowAny",                   # cambiar a IsAuthenticated en Bloque 2
    ),
}

# ─────────────  CORS (bloque 2 lo revisaremos) ─────────
CORS_ALLOW_ALL_ORIGINS = True
º