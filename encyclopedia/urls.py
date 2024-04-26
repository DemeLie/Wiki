from django.urls import path
from .views import read_markdown_file
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('wiki/<str:filename>/', read_markdown_file, name='markdown_file'),
    path('search/', views.search_view, name='search'),
    path('create/', views.create_page, name='create_page'),
    path('edit/<str:title>/', views.edit_page, name='edit_page'),
    path('save_page/<str:title>/', views.save_page, name='save_page'),
    path('random/', views.random_page_choice, name='random_page')
]
