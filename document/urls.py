from django.urls import path
from .views import success, get_file

urlpatterns = [
    path('upload/', get_file, name='upload'),  # This maps to the view that handles file uploads
    path('success/<int:document_id>/', success, name='success'),  # Accept document_id in the URL
]
