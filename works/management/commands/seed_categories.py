from django.core.management.base import BaseCommand
from django.utils.text import slugify
from works.models import Category

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


class Command(BaseCommand):
    help = 'Seed default portfolio categories.'

    def handle(self, *args, **opts):
        for i, name in enumerate(DEFAULT_CATEGORIES):
            Category.objects.get_or_create(
                slug=slugify(name),
                defaults={'name': name, 'sort_order': i},
            )
        self.stdout.write(self.style.SUCCESS('Categories seeded.'))
