# indexer/inverted_index.py
from .preprocessor import Preprocessor
from .models import Term, Posting
from document.models import ExtractedText

def index_document(doc_id):
    """
    Indexes *exactly* the ExtractedText with primary key=doc_id,
    creating or updating Posting rows without touching any other doc.
    """
    doc = ExtractedText.objects.get(pk=doc_id)
    tokens = Preprocessor(doc.text).run_all()

    # Build term -> { frequency, positions } for *this* doc
    term_data = {}
    for pos, token in enumerate(tokens):
        if token not in term_data:
            term_data[token] = {'frequency': 0, 'positions': []}
        term_data[token]['frequency'] += 1
        term_data[token]['positions'].append(pos)

    # Upsert Postings for this one doc
    
    print("here", term_data)
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
