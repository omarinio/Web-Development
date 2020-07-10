from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request, title):
    entry = util.get_entry(title)

    if entry:
        return render(request, "encyclopedia/title.html", {
            "entry": util.get_entry(title),
            "title": title
        })

    else:
        return render(request, "encyclopedia/error.html")

    