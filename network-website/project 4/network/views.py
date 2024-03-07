from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime
from django.core.paginator import Paginator
import json

from .models import User, Post, Like


def index(request):
    
    posts = Post.objects.all().order_by("-timestamp")
    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    all = Like.objects.all()
    yourlikes = []
    for like in all:
        if like.who == request.user:
            yourlikes.append(like.post.id)
  
    
    return render(request, "network/index.html", {
        'page_obj': page_obj,
        'yourlikes': yourlikes        
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


# publish a new post
def newpost(request):
    if request.method == "POST":
        text = request.POST["text"]
        newpost = Post.objects.create(text=text, author=request.user, timestamp=datetime.now())
        newpost.save()
        return HttpResponseRedirect(reverse("index"))



    return render(request, "network/newpost.html")

# show profile
def profile(request, id):
    profile = User.objects.get(id = id)
    posts = profile.network_user_related.all()
    

    if request.method == "POST":
        # follow and change models
        if request.POST.get("follow"):
            profile.followers.add(request.user)
            request.user.followings.add(profile)
        else:
        # unfollow and change models
            profile.followers.remove(request.user)
            request.user.followings.remove(profile)
        



    followerscount = profile.followers.all().count()
    followingscount = profile.followings.all().count()
    return render(request, "network/profile.html", {
        "profile": profile, 
        "posts": posts.order_by("-timestamp"),
        "c": followerscount,
        "s": followingscount
    })

def following(request):
    fs = request.user.followings.all()
    allposts = Post.objects.all().order_by("-timestamp")
    posts = []
    for p in allposts:
        for f in fs:
            if f == p.author:
                posts.append(p)
    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "network/index.html", {
        'page_obj': page_obj
    })


def edit(request, id):
    if request.method == "POST":
        post = Post.objects.get(id=id)
        data = json.loads(request.body)
        post.text = data["content"]
        post.save()
        return JsonResponse({"data": data["content"]})

def like(request, id):
    if request.method == "POST":
        post = Post.objects.get(id=id)
        data = json.loads(request.body)
        
        if data["content"] == "unlike":
            l = Like.objects.get(who=request.user, post=post)
            l.delete()
            
        else:
            l = Like.objects.create(who=request.user, post=post)
            l.save()
        

        return JsonResponse({"data": Like.objects.filter(post=post).count()})

def editprofile(request, id):
    user = User.objects.get(id = request.user.id)
    if request.method == "POST":
        user.username = request.POST["username"]
        user.email = request.POST["email"]
        user.image = request.POST["ava"]
        user.password = request.POST["password"]
        user.color = request.POST["color"]
        user.save()
        return HttpResponseRedirect(reverse("profile", args = (user.id,)))

    user = User.objects.get(id = request.user.id)
    allfields =  [f.name for f in user._meta.get_fields()]
    print(allfields)
    return render(request, "network/editprofile.html", {
        "fields": allfields, 
        "user": user
    })

def main(request):
    return render(request, "network/main.html" )
