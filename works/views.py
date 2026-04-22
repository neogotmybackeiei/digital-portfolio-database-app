from collections import OrderedDict
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q, Prefetch
from django.views.decorators.http import require_POST
from .models import Work, WorkFile, Category
from .forms import WorkForm


def _save_files(work, files):
    for f in files:
        WorkFile.objects.create(work=work, file=f)


def showcase(request):
    pinned = Work.objects.filter(is_pinned=True).order_by('pin_order', '-work_date')[:3]

    categories = Category.objects.prefetch_related(
        Prefetch('works', queryset=Work.objects.order_by('-work_date'))
    )

    grouped = OrderedDict()
    for cat in categories:
        items = list(cat.works.all())
        if items:
            grouped[cat] = items

    uncategorized = Work.objects.filter(category__isnull=True).order_by('-work_date')
    if uncategorized.exists():
        grouped[None] = list(uncategorized)

    return render(request, 'works/showcase.html', {
        'pinned': pinned,
        'grouped': grouped,
    })


def manage_pins(request):
    if request.method == 'POST':
        ids = request.POST.getlist('pinned')[:3]
        Work.objects.update(is_pinned=False, pin_order=0)
        for i, pk in enumerate(ids):
            Work.objects.filter(pk=pk).update(is_pinned=True, pin_order=i)
        messages.success(request, 'Pinned works updated.')
        return redirect('showcase')

    works = Work.objects.all().order_by('-work_date')
    current = list(Work.objects.filter(is_pinned=True).values_list('id', flat=True))
    return render(request, 'works/manage_pins.html', {
        'works': works,
        'current': current,
    })


def timeline(request):
    works = Work.objects.all().order_by('-work_date', '-created_at')
    grouped = OrderedDict()
    for w in works:
        key = w.work_date.strftime('%Y') if w.work_date else 'Undated'
        grouped.setdefault(key, []).append(w)
    return render(request, 'works/timeline.html', {'grouped': grouped})


def filter_view(request):
    qs = Work.objects.all().prefetch_related('files').select_related('category')

    keyword = request.GET.get('q', '').strip()
    category_id = request.GET.get('category', '').strip()
    date_from = request.GET.get('from', '').strip()
    date_to = request.GET.get('to', '').strip()
    file_type = request.GET.get('file_type', '').strip().lower()

    if keyword:
        qs = qs.filter(
            Q(title__icontains=keyword) |
            Q(description__icontains=keyword) |
            Q(keywords__icontains=keyword)
        )
    if category_id:
        qs = qs.filter(category_id=category_id)
    if date_from:
        try:
            qs = qs.filter(work_date__gte=datetime.strptime(date_from, '%Y-%m-%d').date())
        except ValueError:
            pass
    if date_to:
        try:
            qs = qs.filter(work_date__lte=datetime.strptime(date_to, '%Y-%m-%d').date())
        except ValueError:
            pass
    if file_type in ('pdf', 'png', 'jpg', 'jpeg', 'image'):
        if file_type == 'image':
            qs = qs.filter(files__file__iregex=r'\.(png|jpe?g)$').distinct()
        else:
            qs = qs.filter(files__file__iendswith=f'.{file_type}').distinct()

    return render(request, 'works/filter.html', {
        'works': qs.distinct(),
        'categories': Category.objects.all(),
        'q': keyword, 'selected_category': category_id,
        'date_from': date_from, 'date_to': date_to,
        'file_type': file_type,
    })


def work_list(request):
    works = Work.objects.all().select_related('category')
    return render(request, 'works/work_list.html', {'works': works})


def work_detail(request, pk):
    work = get_object_or_404(Work, pk=pk)
    return render(request, 'works/work_detail.html', {'work': work})


def work_create(request):
    if request.method == 'POST':
        form = WorkForm(request.POST, request.FILES)
        files = request.FILES.getlist('files')
        if form.is_valid():
            work = form.save()
            _save_files(work, files)
            messages.success(request, 'Work added.')
            return redirect('work_detail', pk=work.pk)
    else:
        form = WorkForm()
    return render(request, 'works/work_form.html', {'form': form, 'mode': 'create'})


def work_edit(request, pk):
    work = get_object_or_404(Work, pk=pk)
    if request.method == 'POST':
        form = WorkForm(request.POST, request.FILES, instance=work)
        files = request.FILES.getlist('files')
        if form.is_valid():
            work = form.save()
            _save_files(work, files)
            messages.success(request, 'Work updated.')
            return redirect('work_detail', pk=work.pk)
    else:
        form = WorkForm(instance=work)
    return render(request, 'works/work_form.html',
                  {'form': form, 'work': work, 'mode': 'edit'})


@require_POST
def work_delete(request, pk):
    work = get_object_or_404(Work, pk=pk)
    work.delete()
    messages.success(request, 'Work deleted.')
    return redirect('work_list')


@require_POST
def file_delete(request, pk):
    f = get_object_or_404(WorkFile, pk=pk)
    work_pk = f.work_id
    f.delete()
    messages.success(request, 'File removed.')
    return redirect('work_edit', pk=work_pk)
