from django.shortcuts import render, redirect
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def wiki(request, title):
    """ Function that checks if given title is within entries list """
    entries = util.list_entries()
    content = util.get_entry(title)

    if content:
        return render(request, "encyclopedia/entry.html", {"content": content, "title": title})
    else:
        try:
            # Try to find an entry casefolded in entries casefolded
            index = [entry.casefold() for entry in entries].index(title.casefold())
            # Redirect with proper CASE
            return redirect(to="wiki", title=entries[index])

        except ValueError:
            message = "Such entry does not yet exist in encyclopedia"
            return render(request, "encyclopedia/404.html", {"content": message, "title": "Not found"})