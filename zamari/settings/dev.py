from .base import *


DEBUG = True

ALLOWED_HOSTS = []
# ALLOWED_HOSTS = ["52.20.142.99", "ves-tv.ng", "www.ves-tv.ng"]


# INSTALLED_APPS += ["debug_toolbar"]

# MIDDLEWARE += [
#     "debug_toolbar.middleware.DebugToolbarMiddleware",
# ]

# DEBUG_TOOLBAR_PANELS = [
#     "debug_toolbar.panels.versions.VersionsPanel",
#     "debug_toolbar.panels.timer.TimerPanel",
#     "debug_toolbar.panels.settings.SettingsPanel",
#     "debug_toolbar.panels.headers.HeadersPanel",
#     "debug_toolbar.panels.request.RequestPanel",
#     "debug_toolbar.panels.sql.SQLPanel",
#     "debug_toolbar.panels.staticfiles.StaticFilesPanel",
#     "debug_toolbar.panels.templates.TemplatesPanel",
#     "debug_toolbar.panels.cache.CachePanel",
#     "debug_toolbar.panels.signals.SignalsPanel",
#     "debug_toolbar.panels.logging.LoggingPanel",
#     "debug_toolbar.panels.redirects.RedirectsPanel",
# ]


# def show_toolbar(request):
#     return True


# DEBUG_TOOLBAR_CONFIG = {
#     "INTERCEPT_REDIRECTS": False,
#     "SHOW_TOOLBAR_CALLBACK": show_toolbar,
# }


# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db2.sqlite3",
#     }
# }


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST": config("DB_HOST"),
        "PORT": "5432",
    }
}

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = config("EMAIL_HOST")
EMAIL_PORT = config("EMAIL_PORT")
EMAIL_USE_TLS = config("EMAIL_USE_TLS")


DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL")


EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")


ADMINS = (("VESTV Support", "hello@zamari.tv"),)


# CELERY related settings
BROKER_URL = "amqp://localhost"
# CELERY_RESULT_BACKEND = 'amqp://'
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "Africa/Lagos"


AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME")

AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
AWS_S3_REGION_NAME = "us-east-1"
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
