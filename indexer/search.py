# indexer/search.py

import math
from collections import Counter
from .preprocessor import Preprocessor
from .models import Term, Posting
from document.models import ExtractedText

def get_N():
    """Total number of documents in the corpus."""
    return ExtractedText.objects.count()

def get_df(term_str):
    """Document frequency: number of docs containing this term."""
    try:
        term = Term.objects.get(term=term_str)
        return term.postings.count()
    except Term.DoesNotExist:
        return 0

def build_doc_vector(doc):
    """
    Returns { term: tfidf } for a single document.
    """
    N = get_N()
    vec = {}
    postings = Posting.objects.filter(document=doc)
    for p in postings:
        tf = p.frequency
        df = get_df(p.term.term)
        if df == 0:
            continue
        idf = math.log(N / df)
        vec[p.term.term] = tf * idf
    return vec

def build_query_vector(query_text):
    """
    Preprocesses the query and returns its { term: tfidf } vector.
    """
    N = get_N()
    tokens = Preprocessor(query_text).run_all()
    tf_counts = Counter(tokens)
    vec = {}
    for term, tf in tf_counts.items():
        df = get_df(term)
        if df == 0:
            # term not in corpus → skip
            continue
        idf = math.log(N / df)
        vec[term] = tf * idf
    return vec

def cosine_sim(vec1, vec2):
    """
    Cosine similarity between two sparse vectors (dicts).
    """
    # dot product
    dot = sum(vec1[t] * vec2.get(t, 0.0) for t in vec1)
    # norms
    norm1 = math.sqrt(sum(v*v for v in vec1.values()))
    norm2 = math.sqrt(sum(v*v for v in vec2.values()))
    if not norm1 or not norm2:
        return 0.0
    return dot / (norm1 * norm2)

def search(query, top_k=10):
    """
    Returns a list of (document, score) sorted by descending relevance.
    """
    qvec = build_query_vector(query)
    if not qvec:
        return []
    doc_ids = set()
    for term in qvec:
        try:
            term_obj = Term.objects.get(term=term)
            doc_ids.update(term_obj.postings.values_list('document__id', flat=True))
        except Term.DoesNotExist:
            continue

    # score each candidate
    scores = []
    for doc_id in doc_ids:
        doc = ExtractedText.objects.get(pk=doc_id)
        dvec = build_doc_vector(doc)
        score = cosine_sim(qvec, dvec)
        scores.append((doc, score))

    # sort and return top_k
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:top_k]
