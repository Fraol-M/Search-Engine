 # indexer/views.py
from django.shortcuts import render
from django.http import JsonResponse
from .trie import trie
from .search import search

def autocomplete(request):
    prefix = request.GET.get('q', '').strip()
    suggestions = trie.autocomplete(prefix, limit=10) if prefix else []
    return JsonResponse({'results': suggestions})

def search_view(request):
    query = request.GET.get('q', '').strip()
    results = search(query) if query else []
    return render(request, 'search_results.html', {
         'query': query,
         'results': results,
    })
