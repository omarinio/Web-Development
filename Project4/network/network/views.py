import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django import forms

from .models import User, Post, Follow


class PostForm(forms.Form):
    content = forms.CharField(label='', widget=forms.Textarea(attrs={'class' :'form-control'}))


def index(request):
    posts = Post.objects.all()
    return render(request, "network/index.html", {
        "posts": posts,
        "form": PostForm()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@login_required
def new_post(request):
    if request.method == "POST":
        body = request.POST['content']
        Post.objects.create(user=request.user, body = body)

        return HttpResponseRedirect(reverse('index')) 


def user(request, id):
    user_profile = User.objects.get(id=id)

    followers = Follow.objects.filter(user = user_profile).count
    following = Follow.objects.filter(follower = user_profile).count

    user_posts = Post.objects.filter(user = user_profile)

    if request.user.is_authenticated and request.user != user_profile:
        return render(request, "network/user.html", {
            "user": user_profile,
            "followers": followers,
            "following": following,
            "posts": user_posts,
            "can_follow": True
        })
    else:
        return render(request, "network/user.html", {
            "user": user_profile,
            "followers": followers,
            "following": following,
            "posts": user_posts,
            "can_follow": False
        })


@login_required
@csrf_exempt
def follow(request):
    if request.method == "POST":
        data = json.loads(request.body)

        user = data.get("user", "")
        action = data.get("action", "")

        return JsonResponse({'status': 201, 'action': action, 'user': user}, status=201)
