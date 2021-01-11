from django.shortcuts import render, redirect
from . import util
from .forms import SearchForm, NewEntryForm
from django.contrib import messages
from django.core.files.storage import default_storage
from random import choice
from markdown2 import markdown


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def wiki(request, title):
    """ Function that checks if given title is within entries list """
    entries = util.list_entries()
    content = util.get_entry(title)

    util.markdown_to_HTML(content)

    if content:
        return render(request, "encyclopedia/entry.html", {"content": markdown(content), "title": title})
    else:
        try:
            # Try to find an entry casefolded in entries casefolded
            index = [entry.casefold() for entry in entries].index(title.casefold())
            # Redirect with proper CASE
            return redirect(to="wiki", title=entries[index])

        except ValueError:
            message = "Such entry does not yet exist in encyclopedia"
            return render(request, "encyclopedia/404.html", {"content": message, "title": "Not found"})


def search(request):
    title = request.POST['q']
    content = util.get_entry(title)
    if content:
        return redirect(to="wiki", title=title)
    else:
        entries = util.list_entries()
        entries_matched_partially = [entry for entry in entries if title.casefold() in entry.casefold()]
        # print(entries_matched_partially)
        
        return render(request, "encyclopedia/results.html", {
            "results": entries_matched_partially,
            "title": title
        })


def new_entry(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        entries = util.list_entries()

        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']

            if title in entries:
                messages.warning(request, 'This page already exists.')
            else:
                f = default_storage.open(f"entries/{title}.md", "w")
                f.write(content)
                return redirect(to="wiki", title=title)

            return render(request, "encyclopedia/new_entry.html", {"form": form})
            
    else:
        form = NewEntryForm()
        return render(request, "encyclopedia/new_entry.html", {
            "form": form
        })


def edit_entry(request, title):
    content = util.get_entry(title)

    form = NewEntryForm({"title": title, "content": content})

    return render(request, "encyclopedia/edit_entry.html", {
        "form": form
    })


def save_changes(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']

            f = default_storage.open(f"entries/{title}.md", "w")
            f.write(content)
            
            return redirect(to="wiki", title=title)


def random_page(request):
    entries = util.list_entries()
    random_title = choice(entries)
    return redirect(to="wiki", title=random_title)

    