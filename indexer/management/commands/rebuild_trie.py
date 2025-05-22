from django.core.management.base import BaseCommand
from indexer.models import Term, Posting
from indexer.trie import trie

class Command(BaseCommand):
    help = 'Rebuilds the in-memory Trie from all existing Terms and their total frequencies'

    def handle(self, *args, **options):
        # Reset the trie
        trie.root = trie.__class__().root
        self.stdout.write('Cleared existing Trie')

        # Aggregate frequencies and insert
        terms = Term.objects.all().prefetch_related('postings')
        count = 0
        for term in terms:
            total_freq = sum(p.frequency for p in term.postings.all())
            if total_freq:
                trie.insert_with_count(term.term, total_freq)
                count += 1
        self.stdout.write(f'Rebuilt Trie with {count} terms')