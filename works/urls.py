from django.urls import path
from . import views

urlpatterns = [
    path('', views.showcase, name='showcase'),
    path('timeline/', views.timeline, name='timeline'),
    path('filter/', views.filter_view, name='filter'),
    path('pin/', views.manage_pins, name='manage_pins'),

    path('works/', views.work_list, name='work_list'),
    path('works/add/', views.work_create, name='work_create'),
    path('works/<int:pk>/', views.work_detail, name='work_detail'),
    path('works/<int:pk>/edit/', views.work_edit, name='work_edit'),
    path('works/<int:pk>/delete/', views.work_delete, name='work_delete'),
    path('works/files/<int:pk>/delete/', views.file_delete, name='file_delete'),
]
