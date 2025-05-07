# # indexer/models.py
from django.db import models
from document.models import ExtractedText

class Term(models.Model):
    term = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.term

class Posting(models.Model):
    term = models.ForeignKey(Term, on_delete=models.CASCADE, related_name='postings')
    document = models.ForeignKey(ExtractedText, on_delete=models.CASCADE, related_name='postings')
    frequency = models.IntegerField(default=0)
    positions = models.JSONField(default=list)

    class Meta:
        unique_together = ('term', 'document')

    def __str__(self):
        return f"'{self.term.term}' in document {self.document.id}: freq={self.frequency}, pos={self.positions}"

