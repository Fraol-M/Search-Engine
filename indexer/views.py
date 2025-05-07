# views.py
from django.shortcuts import render
from indexer.search import search  


def search_view(request):
    query = request.GET.get('q', '')  # 'q' is the name of your input field
    results = []
    
    if query:
        results = search(query)  # Returns list of (doc, score)

    return render(request, 'search_results.html', {
        'query': query,
        'results': results
    })
