# indexer/apps.py

from django.apps import AppConfig

class IndexerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'indexer'

    def ready(self):
        import indexer.signals  # noqa



class IndexerConfig(AppConfig):
    name = 'indexer'

    def ready(self):
        from indexer.models import Term
        from indexer.trie import trie

        terms = Term.objects.all().prefetch_related('postings')
        for term in terms:
            total_freq = sum(p.frequency for p in term.postings.all())
            if total_freq:
                trie.insert_with_count(term.term, total_freq)
