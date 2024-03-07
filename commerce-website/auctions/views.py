from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from datetime import datetime

from .models import User, Category, Auction, Bid, Watchlist, Comment

# form for creating new auction listing
class NewListingForm(forms.Form):
    title = forms.CharField(label="Title")
    description = forms.CharField(label="Description", widget=forms.Textarea)
    bid = forms.DecimalField(label="Bid")
    image = forms.URLField(label="Link to an image", required=False)

class NewBidForm(forms.Form):
    bid = forms.DecimalField(label="Bid")
    

def index(request):
    return render(request, "auctions/index.html", {
        "listings": Auction.objects.all()
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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


# create a new auction listing
def create(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        bid = request.POST["bid"]
        image = request.POST["image"]

        # i want to add several different categories while creating a new object but at the moment i receive only errors!!!!!!!!!!
        categoryfromform = request.POST["category"]
        category = Category.objects.get(pk=categoryfromform)
        owner = User.objects.get(username=request.user)

        #bid object first
        b = Bid(bid=bid, user=owner)
        b.save()

        auction = Auction(title=title, description=description, image=image, category=category, owner = owner)
        auction.save()
        auction.price.set([b])
        auction.save()

    return render(request, "auctions/create.html", {
        "form": NewListingForm(), 
        "categorys": Category.objects.all()
    })


def listing(request, title):
    a = Auction.objects.get(title=title)
    if request.user.is_authenticated:
        iswatched = Watchlist.objects.filter(auction = a, user = request.user)
    else:
        iswatched = False
    price = a.price.get()

    return render(request, "auctions/listing.html", {
        "listing": Auction.objects.get(title=title),
        "price": price,
        "iswatched": iswatched,
        "comments": Comment.objects.filter(auction = a),
        "form": NewBidForm()
    })

@login_required
def addWatchlist(request, id):
    currentuser = User.objects.get(username=request.user)
    listing = Auction.objects.get(pk=id)
    b = Watchlist(auction=listing, user = currentuser)
    b.save()
    return HttpResponseRedirect(reverse("listing", args=(listing.title,)))

@login_required
def removeWatchlist(request, id):
    currentuser = User.objects.get(username=request.user)
    listing = Auction.objects.get(pk=id)
    Watchlist.objects.filter(auction=listing, user = currentuser).delete()
    return HttpResponseRedirect(reverse("listing", args=(listing.title,)))

@login_required
def comment(request, id):
    currentuser = User.objects.get(username=request.user)
    listing = Auction.objects.get(pk=id)
    text = request.POST["comment"]
    now = datetime.now()
    newcomment = Comment(auction=listing, text=text, user=currentuser, time=now)
    newcomment.save()
    return HttpResponseRedirect(reverse("listing", args=(listing.title,)))

@login_required
def addBid(request, id):
    currentuser = User.objects.get(username=request.user)
    listing = Auction.objects.get(pk=id)
    currentprice = listing.price.get()   
    bid = request.POST["bid"]
    if int(bid) > currentprice.bid:
        newBid = Bid(bid=bid, user=currentuser)
        newBid.save()
        listing.price.set([newBid])
        listing.save()
    else:
        iswatched = Watchlist.objects.filter(auction = listing, user = currentuser)
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "price": currentprice,
            "iswatched": iswatched,
            "comments": Comment.objects.filter(auction = listing),
            "form": NewBidForm(),
            "message": "Your bid must be higher than the current price"
        })
    return HttpResponseRedirect(reverse("listing", args=(listing.title,)))

@login_required
def close(request, id):
    listing = Auction.objects.get(pk=id)
    w = listing.price.get()
    listing.winner = w.user
    listing.status = False
    listing.save()
    return render(request, "auctions/index.html")


def category(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all()
    })

def speccategory(request, category):
    listings = Auction.objects.filter(category=category)
    return render(request, "auctions/speccategory.html", {
        "listings": listings
    })

@login_required
def MyWatchlist(request):
    user = request.user
    listings = Watchlist.objects.filter(user = user)
    print(listings)
    return render(request, "auctions/watchlist.html",{
        "listings": listings
    })



