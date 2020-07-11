from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django import forms
from random import choice

from . import util


# defines the search form so it can be edited in python instead of html
class SearchForm(forms.Form):
    q = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Search encyclopedia'}))

# returns the index website request
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchForm()
    })

# returns webpage with for the specified title
def title(request, title):
    # gets the entry 
    entry = util.get_entry(title)

    # returns the corresponding page if entry exists, otherwise shows generic error page
    if entry:
        return render(request, "encyclopedia/title.html", {
            "entry": util.get_entry(title),
            "title": title,
            "form": SearchForm()
        })

    else:
        return render(request, "encyclopedia/error.html", {
            "form": SearchForm()
        })

# search method, either displays correct page or potential search results
def search(request, query):
    # checks if request is a POST method
    if request.method=="POST":
        # saves data as form
        form = SearchForm(request.POST)

        if form.is_valid():
            query = form.cleaned_data["q"]

            # makes data lowercase to prevent case sensitivity
            lowercase_data = [e.lower() for e in util.list_entries()]
            
            # if query exists, redirect to title url page
            # kwargs is used to pass keyworded variables
            if query.lower() in lowercase_data:
                return redirect(reverse("encyclopedia:title", kwargs={
                    "title": query
                }))
        
            else:
                substrings = [s for s in util.list_entries() if query in s.lower()]

                return render(request, "encyclopedia/search.html", {
                    "entries": substrings,
                    "form": SearchForm()
                })

    else:
        return render(request, "encyclopedia/error.html", {
            "form": SearchForm()
        })

def random(request):
    return redirect(reverse("encyclopedia:title", kwargs={
        "title": choice(util.list_entries())
    }))