from django.apps import AppConfig
from django.db import connection, OperationalError, ProgrammingError
from django.utils.text import slugify

DEFAULT_CATEGORIES = [
    'Article',
    'Academic Writing',
    'Diagram',
    'Graphic Design',
    'Photography',
    'Video Production',
    'Client Work',
    'Research Project',
    'Data Visualization',
    'Programming Projects',
    'Other',
]


class WorksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'works'

    def ready(self):
        try:
            from .models import Category

            table_name = Category._meta.db_table
            with connection.cursor() as cursor:
                if table_name not in connection.introspection.table_names(cursor):
                    return

            if Category.objects.exists():
                return

            for i, name in enumerate(DEFAULT_CATEGORIES):
                Category.objects.get_or_create(
                    slug=slugify(name),
                    defaults={'name': name, 'sort_order': i},
                )
        except (OperationalError, ProgrammingError):
            pass
