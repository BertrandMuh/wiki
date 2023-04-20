from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path('search', views.search, name='search'),
    path('new-page', views.newEntry, name='add-entry'),
    path('error', views.error, name='error'),
    path('wiki/<str:title>/edit', views.edit, name='edit'),
    path('random', views.randomEntry, name='random-entry')
]
