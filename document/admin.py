from django.contrib import admin

from .models import Document, ExtractedText

# Register your models here.

admin.site.register(Document)
admin.site.register(ExtractedText)
