from django.db import models

class Document(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/')  # Store the PDF in a 'documents' folder
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



class ExtractedText(models.Model):
    pdf = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='extracted_texts')
    text = models.TextField()
    
    
    def __str__(self):
        return f"Extracted Text for {self.pdf.title}"