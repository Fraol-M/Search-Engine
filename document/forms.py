from django import forms
from .models import Document

class Uploadfile(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'file']
        
    
    