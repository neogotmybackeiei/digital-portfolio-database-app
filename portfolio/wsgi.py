import os
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.settings')

django_app = get_wsgi_application()

application = WhiteNoise(django_app, root=settings.STATIC_ROOT)
