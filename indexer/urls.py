# indexer/urls.py

from django.urls import path
from .views import search_view, autocomplete

urlpatterns = [
    path("search/", search_view, name='search'),
    path('autocomplete/', autocomplete, name='autocomplete'),

]
