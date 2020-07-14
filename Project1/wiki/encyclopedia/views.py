from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django import forms
from random import choice
import markdown2

from . import util


# defines the search form so it can be edited in python instead of html
class SearchForm(forms.Form):
    q = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Search encyclopedia'}))

class CreateForm(forms.Form):
    title = forms.CharField(label='Title', widget=forms.TextInput(attrs={'placeholder': 'Title'}))
    textarea = forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder': 'Markdown Contents', 'style': 'height:500px'}))

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
        mdentry = markdown2.markdown(entry)
        return render(request, "encyclopedia/title.html", {
            "entry": mdentry,
            "title": title,
            "form": SearchForm()
        })

    else:
        return render(request, "encyclopedia/error.html", {
            "form": SearchForm(),
            "error": "Error 404, page not found..."
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
            "form": SearchForm(),
            "error": "POST method failure"
        })

def random(request):
    return redirect(reverse("encyclopedia:title", kwargs={
        "title": choice(util.list_entries())
    }))

def create(request):
    if request.method == "POST":
        form = CreateForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            lowercase_data = [e.lower() for e in util.list_entries()]

            if title.lower() in lowercase_data:
                return render(request, "encyclopedia/error.html", {
                    "form": SearchForm(),
                    "error": "Page with this name already exists."
                })

            textarea = form.cleaned_data["textarea"]

            util.save_entry(title, textarea)

            return redirect(reverse("encyclopedia:title", kwargs={
                "title": title
            }))

        else:
            return render(request, "encyclopedia/error.html", {
            "form": SearchForm(),
            "error": "Form is invalid, please try again."
        })

    return render(request, "encyclopedia/create.html", {
        "createform": CreateForm(),
        "form": SearchForm()
    })

def edit(request, title):
    if request.method == "POST":
        form = CreateForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]

            textarea = form.cleaned_data["textarea"]

            util.save_entry(title, textarea)

            return redirect(reverse("encyclopedia:title", kwargs={
                "title": title
            }))

        else:
            return render(request, "encyclopedia/error.html", {
            "form": SearchForm(),
            "error": "Form is invalid, please try again."
        })

    textarea = util.get_entry(title)

    if textarea:
        return render(request, "encyclopedia/edit.html", {
            "createform": CreateForm(initial={
                "title": title,
                "textarea": textarea
            }),
            "form": SearchForm(),
            "title": title
        })
    
    else:
        return render(request, "encyclopedia/error.html", {
            "form": SearchForm(),
            "error": "Error 404, page not found..."
        })
        

