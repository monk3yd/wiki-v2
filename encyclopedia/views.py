from markdown2 import Markdown

from django import forms
from django.http import Http404
from django.shortcuts import render, HttpResponseRedirect, redirect

from . import util


def index(request):
    if request.method == "POST":
        entries = util.list_entries()
        lower_entries = [entry.lower() for entry in entries]
        
        # Get inputted search value from request
        query = request.POST.get('q').lower()

        # Check if query exists in articles
        if query in lower_entries:
            index = lower_entries.index(query)
            title = entries[index]
            return redirect('article', title=title)

        # List of all articles with searched substring
        sub_entries = []
        # Check if query is a substring of one or more articles
        for idx, entry in enumerate(lower_entries):
            # print(idx, entry)
            if query in entry:
                # print(query)
                sub_entries.append(entries[idx])
        # print(sub_entries)
        # redirect to search page (list of all entries with substring)
        return render(request, 'encyclopedia/search.html', {
            "entries": sub_entries
        })

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def article(request, title):
    markdowner = Markdown()
    # Get entry
    markdown_entry = util.get_entry(title)
    
    # If entry doesn't exist
    if markdown_entry == None:
        raise Http404("Error 404. This entry doesn't exist yet.")
    # Else 
    
    # Convert entry to html
    entry = markdowner.convert(markdown_entry)  # Convert Markdown into HTML
    
    # render the content of the entry
    return render(request, "encyclopedia/article.html", {
        "entry": entry
    })


def search(request, entries):
    return render(request, "encyclopedia/search.html", entries=entries)