from markdown2 import Markdown

from django import forms
from django.contrib import messages
from django.http import Http404
from django.shortcuts import render, HttpResponseRedirect, redirect

import random

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
        # go to search page (list of all entries with substring)
        return render(request, "encyclopedia/search.html", {
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
    html = markdowner.convert(markdown_entry)  # Convert Markdown into HTML

    # render the content of the entry
    return render(request, "encyclopedia/article.html", {
        "title": title,
        "entry": html
    })


def create(request):
    if request.method == "POST":
        entries = util.list_entries()
        lower_entries = [entry.lower() for entry in entries]

        title = request.POST.get('new-entry-title')
        # If article already exists
        if title.lower() in lower_entries:
            messages.info(request, 'Error. Article already exists.')
            return render(request, "encyclopedia/create.html")

        markdown_text = request.POST.get('textarea')

        print(title)
        print(markdown_text)

        # Save new article entry
        util.save_entry(title, markdown_text)
        return redirect('article', title=title)

    return render(request, "encyclopedia/create.html")


def edit(request, title):
    if request.method == "POST":
        title = request.POST.get('new-entry-title')
        textarea = request.POST.get('textarea')
        util.save_entry(title, textarea)
        return redirect('article', title=title)

    entry = util.get_entry(title)
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "entry": entry
    })


def rand(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    return redirect('article', title=random_entry)
