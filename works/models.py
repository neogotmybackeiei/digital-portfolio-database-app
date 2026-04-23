import os
import io
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.core.files.base import ContentFile
 
try:
    from pdf2image import convert_from_bytes
    PDF2IMAGE_AVAILABLE = True
except ImportError:
    PDF2IMAGE_AVAILABLE = False
 
 
class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=90, unique=True)
    sort_order = models.PositiveIntegerField(default=0)
 
    class Meta:
        ordering = ['sort_order', 'name']
        verbose_name_plural = 'categories'
 
    def __str__(self):
        return self.name
 
 
class Work(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    keywords = models.CharField(
        max_length=255, blank=True,
        help_text='Comma-separated keywords (e.g. branding, motion, print)',
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='works',
    )
    link = models.URLField(blank=True)
    work_date = models.DateField(
        default=timezone.now,
        help_text='Date the work was created or completed',
    )
 
    # Pin to homepage (only top 3 by pin_order are shown as "Featured")
    is_pinned = models.BooleanField(default=False)
    pin_order = models.PositiveIntegerField(default=0)
 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    class Meta:
        ordering = ['-work_date', '-created_at']
 
    def __str__(self):
        return self.title
 
    def get_absolute_url(self):
        return reverse('work_detail', args=[self.pk])
 
    def keyword_list(self):
        return [k.strip() for k in self.keywords.split(',') if k.strip()]
 
 
def work_file_upload_to(instance, filename):
    return f'works/{instance.work_id}/{filename}'
 
 
class WorkFile(models.Model):
    work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to=work_file_upload_to)
    thumbnail = models.ImageField(upload_to=work_file_upload_to, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
 
    class Meta:
        ordering = ['uploaded_at']
 
    def __str__(self):
        return os.path.basename(self.file.name)
 
    @property
    def extension(self):
        return os.path.splitext(self.file.name)[1].lower().lstrip('.')
 
    @property
    def is_image(self):
        return self.extension in ('png', 'jpg', 'jpeg')
 
    @property
    def is_pdf(self):
        return self.extension == 'pdf'
 
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
 
        if self.thumbnail:
            return  # already has a thumbnail, nothing to do
 
        if self.is_image:
            # For images: generate a resized thumbnail in memory using Pillow
            try:
                from PIL import Image
                self.file.seek(0)
                img = Image.open(self.file)
                img.thumbnail((300, 300))
                thumb_io = io.BytesIO()
                fmt = 'JPEG' if self.extension in ('jpg', 'jpeg') else 'PNG'
                img.save(thumb_io, format=fmt)
                thumb_io.seek(0)
                thumb_filename = (
                    os.path.splitext(os.path.basename(self.file.name))[0]
                    + '_thumb.'
                    + ('jpg' if fmt == 'JPEG' else 'png')
                )
                self.thumbnail.save(thumb_filename, ContentFile(thumb_io.read()), save=False)
                super().save(update_fields=['thumbnail'])
            except Exception:
                pass  # thumbnail is optional; never crash the upload
 
        elif self.is_pdf and PDF2IMAGE_AVAILABLE:
            # For PDFs: read bytes from storage, convert first page in memory
            try:
                self.file.seek(0)
                pdf_bytes = self.file.read()
                images = convert_from_bytes(pdf_bytes, first_page=1, last_page=1, size=(300, None))
                if images:
                    thumb_io = io.BytesIO()
                    images[0].save(thumb_io, 'JPEG')
                    thumb_io.seek(0)
                    thumb_filename = (
                        os.path.splitext(os.path.basename(self.file.name))[0]
                        + '_thumb.jpg'
                    )
                    self.thumbnail.save(thumb_filename, ContentFile(thumb_io.read()), save=False)
                    super().save(update_fields=['thumbnail'])
            except Exception:
                pass  # thumbnail is optional; never crash the upload
