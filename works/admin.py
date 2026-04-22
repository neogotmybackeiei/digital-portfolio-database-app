from django.contrib import admin
from .models import Work, WorkFile, Category


class WorkFileInline(admin.TabularInline):
    model = WorkFile
    extra = 1


@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'work_date', 'is_pinned', 'pin_order')
    list_filter = ('category', 'is_pinned')
    search_fields = ('title', 'description', 'keywords')
    inlines = [WorkFileInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'sort_order')
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(WorkFile)
