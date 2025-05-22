from .preprocessor import Preprocessor
from .models import Term, Posting
from document.models import ExtractedText
from .trie import trie

def index_document(doc_id):
    
    doc = ExtractedText.objects.get(pk=doc_id)
    tokens = Preprocessor(doc.text).run_all()

    term_data = {}
    for pos, token in enumerate(tokens):
        if token not in term_data:
            term_data[token] = {'frequency': 0, 'positions': []}
        term_data[token]['frequency'] += 1
        term_data[token]['positions'].append(pos)

    # Upsert postings and update Trie
    for token, data in term_data.items():
        term_obj, _ = Term.objects.get_or_create(term=token)
        Posting.objects.update_or_create(
            term=term_obj,
            document=doc,
            defaults={
                'frequency': data['frequency'],
                'positions': data['positions'],
            }
        )
        
        trie.insert_with_count(token, data['frequency'])