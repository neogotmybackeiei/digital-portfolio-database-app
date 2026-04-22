import os
from django import forms
from .models import Work, Category

ALLOWED_EXT = {'pdf', 'png', 'jpg', 'jpeg'}
MAX_SIZE = 10 * 1024 * 1024  # 10MB


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('widget', MultipleFileInput(attrs={'multiple': True}))
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single = super().clean
        if isinstance(data, (list, tuple)):
            return [single(d, initial) for d in data]
        return [single(data, initial)] if data else []


class WorkForm(forms.ModelForm):
    files = MultipleFileField(
        required=False,
        help_text='Add one or more files (pdf, png, jpg, jpeg). Max 10MB each.',
    )

    class Meta:
        model = Work
        fields = ['title', 'description', 'keywords', 'category',
                  'link', 'work_date', 'is_pinned']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'work_date': forms.DateInput(attrs={'type': 'date'}),
            'category': forms.Select(),
        }

    def clean_files(self):
        files = self.cleaned_data.get('files') or []
        for f in files:
            ext = os.path.splitext(f.name)[1].lower().lstrip('.')
            if ext not in ALLOWED_EXT:
                raise forms.ValidationError(
                    f'"{f.name}" has unsupported type .{ext}. '
                    f'Allowed: {", ".join(sorted(ALLOWED_EXT))}.'
                )
            if f.size > MAX_SIZE:
                raise forms.ValidationError(
                    f'"{f.name}" is larger than 10MB.'
                )
        return files


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug', 'sort_order']
