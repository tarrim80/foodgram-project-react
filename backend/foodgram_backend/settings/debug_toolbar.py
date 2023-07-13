from foodgram_backend.settings import base

if base.DEBUG:
    base.INSTALLED_APPS += ('debug_toolbar',)

    base.MIDDLEWARE += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )

    INTERNAL_IPS = ('127.0.0.1',)
