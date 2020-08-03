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
from django.core.paginator import Paginator

from .models import User, Post, Follow


class PostForm(forms.Form):
    content = forms.CharField(label='', widget=forms.Textarea(attrs={'class' :'form-control'}))


def index(request):
    posts = Post.objects.all().order_by('-timestamp')
    paginated_posts = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_posts = paginated_posts.get_page(page_number)

    return render(request, "network/index.html", {
        "posts": page_posts,
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


@login_required(login_url='login')
def new_post(request):
    if request.method == "POST":
        body = request.POST['content']
        Post.objects.create(user=request.user, body = body)

        return HttpResponseRedirect(reverse('index')) 


def user(request, id):
    user_profile = User.objects.get(id=id)

    followers = Follow.objects.filter(user = user_profile).count
    following = Follow.objects.filter(follower = user_profile).count

    user_posts = Post.objects.filter(user = user_profile).order_by('-timestamp')

    paginated_posts = Paginator(user_posts, 10)

    page_number = request.GET.get('page')
    page_posts = paginated_posts.get_page(page_number)

    if request.user.is_authenticated and request.user != user_profile:
        is_following = False

        if Follow.objects.filter(user = user_profile, follower = request.user).count() > 0:
            is_following = True

        return render(request, "network/user.html", {
            "user_profile": user_profile,
            "followers": followers,
            "following": following,
            "posts": page_posts,
            "can_follow": True,
            "is_following": is_following
        })
    else:
        return render(request, "network/user.html", {
            "user_profile": user_profile,
            "followers": followers,
            "following": following,
            "posts": page_posts,
            "can_follow": False
        })


@login_required(login_url='login')
def follow(request):
    if request.method == "POST":
        data = json.loads(request.body)

        user = data.get("user", "")
        action = data.get("action", "")

        if action == "Follow":
            try:
                if Follow.objects.filter(user = User.objects.get(username = user), follower = request.user).count() == 0:
                    Follow.objects.create(user = User.objects.get(username = user), follower = request.user)
                    
                    return JsonResponse({'status': 201, 'action': "Unfollow", 'followers': Follow.objects.filter(user = User.objects.get(username = user)).count()}, status=201)
                else:
                    return JsonResponse({'message': "You are already following this user!"}, status=400)
            except:
                return JsonResponse({}, status=404)
        else:
            try:
                if Follow.objects.filter(user = User.objects.get(username = user), follower = request.user).count() > 0:
                    follow_to_delete = Follow.objects.get(user = User.objects.get(username = user), follower = request.user)
                    follow_to_delete.delete()

                    return JsonResponse({'status': 201, 'action': "Follow", 'followers': Follow.objects.filter(user = User.objects.get(username = user)).count()}, status=201)
                else: 
                    return JsonResponse({'message': "You cannot unfollow a user you are not following!"}, status=400)
            except:
                return JsonResponse({}, status=404)

    return JsonResponse({}, status=400)


@login_required(login_url='login')
def following(request):
    following_users = Follow.objects.filter(follower = request.user)
    posts = []
    for user in following_users:
        user_posts = Post.objects.filter(user = user.user)
        for post in user_posts:
            posts.append(post)

    posts.sort(key = lambda x: x.timestamp)

    posts = posts[::-1]

    paginated_posts = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_posts = paginated_posts.get_page(page_number)

    return render(request, "network/following.html", {
            "posts": page_posts
        })


@login_required(login_url='login')
def edit(request):
    if request.method != "PUT":
        return JsonResponse({'message': "Must access through PUT request"}, status = 400)

    data = json.loads(request.body)

    try:
        post_id = data.get("post_id", "")
        post = data.get("post", "")
        edited_post = Post.objects.get(id = post_id)
        if request.user == edited_post.user:
            edited_post.body = post
            edited_post.save()
            return JsonResponse({}, status = 201)
        else:
            return JsonResponse({'message': "Access denied"}, status = 403)
    except:
        return JsonResponse({'message': "Post not found"}, status = 404)


@login_required(login_url='login')
def like(request):
    if request.method != "PUT":
        return JsonResponse({"status": 400, 'message': "Must access through PUT request"}, status = 400)

    data = json.loads(request.body)

    post_id = data.get("post_id", "")
    action = data.get("action", "")
    
    try:       
        post = Post.objects.get(id = post_id)
    except:
        return JsonResponse({"status": 404, 'message': "Post not found"}, status = 404)

    if action == "like":
        try:
            if request.user in post.likes.all():
                return JsonResponse({"status": 400, 'message': "You already liked this post!"}, status=400)
            else:
                post.likes.add(request.user)
                post.save()
                return JsonResponse({"status": 201}, status = 201)
        except:
            return JsonResponse({"status": 400, 'message': "Something has gone wrong..."}, status=400)
    else:
        try:
            if request.user in post.likes.all():
                post.likes.remove(request.user)
                post.save()
                return JsonResponse({"status": 201}, status = 201)
            else:
                return JsonResponse({"status": 400, 'message': "You cannot unlike a post you haven't liked!"}, status=400)
        except:
            return JsonResponse({"status": 400, 'message': "Something has gone wrong..."}, status=400)