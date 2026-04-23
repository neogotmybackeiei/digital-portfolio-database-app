
import os
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise
from django.conf import settings
 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.settings')
 
django_app = get_wsgi_application()
 
# Serve static files
application = WhiteNoise(django_app, root=settings.STATIC_ROOT)
 
# Also serve media files from the Railway volume
application.add_files(settings.MEDIA_ROOT, prefix=settings.MEDIA_URL)
 
