#signal.py
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Posting
from .trie import trie

@receiver(post_delete, sender=Posting)
def remove_from_trie(sender, instance, **kwargs):
    """
    Decrement or remove terms from the Trie when a Posting is deleted.
    NOTE: If a document is reindexed, you may prefer to rebuild the whole Trie.
    """
    token = instance.term.term
    freq = instance.frequency
    # If you need a remove_with_count, implement similarly to insert_with_count but subtract
    # For now, we won't remove—rebuild on-demand instead.
    pass  # optional: implement removal logic or rely on rebuild command