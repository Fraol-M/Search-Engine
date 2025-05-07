from django.contrib import admin
from .models import Term, Posting

@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    list_display = ('term',)

@admin.register(Posting)
class PostingAdmin(admin.ModelAdmin):
    list_display = ('term', 'document', 'frequency', 'positions')
    list_filter = ('term', 'document')
    search_fields = ('term__term', 'document__id')
