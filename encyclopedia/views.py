from django.shortcuts import render, redirect
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def wiki(request, title):
    # Get all entries
    entries = util.list_entries()

    try:
        # Try to find an entry casefolded in entries casefolded
        index = [entry.casefold() for entry in entries].index(title.casefold())



        # Get casefolded entry
        content = util.get_entry(entries[index])
        return render(request, "encyclopedia/entry.html", {"content": content, "title": title})

    except ValueError:
        message = "404 - Such entry does not exist in encyclopedia"
        return render(request, "encyclopedia/404.html", {"content": message, "title": "Not found"})



class Entry:
    def __init__(self, title):
        self.title = title

    def is_casefolded_in_entries(self, entries):
        casefolded =  [entry.casefold() for entry in entries]
    

    def is_exact_in_entries(self, entries):
        pass