from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required
from django.forms import modelform_factory
from django.db.models import Max

from .models import User, AuctionListing, Bid, Comment, Watchlist


class ListingForm(forms.Form):
    listing_title = forms.CharField(label = "", widget=forms.TextInput(attrs={'placeholder': 'Listing name'}))
    listing_description = forms.CharField(label = "", widget=forms.Textarea(attrs={'placeholder': 'Listing description (512 chars max)', 'style': 'width: 500px'}))
    starting_bid = forms.DecimalField(label = "", widget=forms.NumberInput(attrs={'placeholder': 'Starting bid', 'style': 'width:300px'}), decimal_places=2, max_digits=8)
    listing_image = forms.URLField(label = "", widget=forms.TextInput(attrs={'placeholder': 'Image URL'}), required=False)

class BidForm(forms.Form):
    new_bid_amount = forms.DecimalField(label = "", widget=forms.NumberInput(attrs={'placeholder': 'Bid', 'style': 'width:300px'}), decimal_places=2, max_digits=8)

class CommentForm(forms.Form):
    comment_content = forms.CharField(label = "", widget=forms.Textarea(attrs={'placeholder': 'Post a comment (256 chars max)', 'style': 'width: 500px'}))


def index(request):
    return render(request, "auctions/index.html", {
        "listings": AuctionListing.objects.filter(closed=False)
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


def listing(request, id):
    # gets the listing requested by checking id
    listing = AuctionListing.objects.get(id=id)

    # gets all bids for specific listing
    bids = Bid.objects.filter(item=listing)
    max_bid = listing.starting_bid

    # check which bid is highest
    for bid in bids:
        if bid.bid_amount > max_bid:
            max_bid = bid.bid_amount

    # gets current user
    current_user = request.user
    can_close = False

    # allows user to close current listing if they are owner of listing
    if current_user == listing.seller:
        can_close = True

    # checks if user has listing in watchlist
    is_watchlisted = False
    if Watchlist.objects.filter(item=listing, user=request.user):
        is_watchlisted = True

    comments = Comment.objects.filter(item=listing)

    winner = None
    if listing.closed:
        winner_listings = Bid.objects.filter(item=listing)
        winner = winner_listings.last()

    return render(request, "auctions/listing.html", {
                "listing": listing,
                "max_bid": max_bid,
                "can_close": can_close,
                "message": "",
                "bid_form": BidForm(),
                "comment_form": CommentForm(),
                "comments": comments,
                "is_watchlisted": is_watchlisted,
                "is_closed": listing.closed,
                "winner": winner,
                "user": request.user
            })


def categories(request):
    categories = ['Fashion', 'Toys', 'Electronics', 'Home', 'Sporting Goods', 'Vehicles']

    return render(request, "auctions/categories.html", {
        "categories": categories
    })


def category_view(request, category):
    listings = AuctionListing.objects.filter(categories=category)

    return render(request, "auctions/category_view.html", {
        "category": category,
        "listings": listings
    })


@login_required
def create_listing(request):
    if request.method == "POST":
        new_listing = ListingForm(request.POST)

        if new_listing.is_valid():
            new_listing_title = new_listing.cleaned_data["listing_title"]
            new_listing_description = new_listing.cleaned_data["listing_description"]
            new_starting_bid = new_listing.cleaned_data["starting_bid"]
            new_listing_image = new_listing.cleaned_data["listing_image"]
            new_category = request.POST["category"]

            new_listing_object = AuctionListing(name = new_listing_title, description = new_listing_description, starting_bid = new_starting_bid,
                                    image = new_listing_image, seller = request.user, categories = new_category)
            new_listing_object.save()

            return HttpResponseRedirect(reverse("index"))
    
    categories = ['Fashion', 'Toys', 'Electronics', 'Home', 'Sporting Goods', 'Vehicles']

    return render(request, "auctions/create.html", {
        "listing_form": ListingForm(),
        "categories": categories
    })


@login_required
def bid(request, id):
    if request.method == "POST":
        new_bid = BidForm(request.POST)
        
        if new_bid.is_valid():
            new_bid_amount = float(new_bid.cleaned_data["new_bid_amount"])
            listing = AuctionListing.objects.get(id=id)
            current_user = request.user

            bids = Bid.objects.filter(item=listing)
            max_bid = listing.starting_bid

            for bid in bids:
                if bid.bid_amount > max_bid:
                    max_bid = bid.bid_amount

            comments = Comment.objects.filter(item=listing)

            is_watchlisted = False
            if Watchlist.objects.filter(item=listing, user=request.user):
                is_watchlisted = True
                        
            if new_bid_amount > max_bid:
                created_bid = Bid(user = current_user, item = listing, bid_amount = new_bid_amount)
                created_bid.save()

                # return HttpResponseRedirect(reverse("listing", args=(id,)))
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "max_bid": new_bid_amount,
                    "message": "Bid was successful!",
                    "bid_form": BidForm(),
                    "comment_form": CommentForm(),
                    "comments": comments,
                    "is_watchlisted": is_watchlisted,
                    "is_closed": listing.closed
                })
            else:
                # return HttpResponseRedirect(reverse("listing", args=(id,)))
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "max_bid": max_bid,
                    "message": f"Your bid amount was lower than the highest bid offer of ${max_bid}",
                    "bid_form": BidForm(),
                    "comment_form": CommentForm(),
                    "comments": comments,
                    "is_watchlisted": is_watchlisted,
                    "is_closed": listing.closed
                })


@login_required
def add_comment(request, id):
    if request.method == "POST":
        comment = CommentForm(request.POST)

        if comment.is_valid():
            new_comment = comment.cleaned_data["comment_content"]
            listing = AuctionListing.objects.get(id=id)

            new_comment_object = Comment(user = request.user, item = listing, comment = new_comment)
            new_comment_object.save()

            return HttpResponseRedirect(reverse("listing", args=(id,)))


@login_required
def add_watchlist(request, id):
    if request.method == "POST":
        item_to_watchlist = AuctionListing.objects.get(id=id)
        new_watchlist = Watchlist(user = request.user, item = item_to_watchlist)
        new_watchlist.save()

        return HttpResponseRedirect(reverse("listing", args=(id,)))


@login_required
def delete_watchlist(request, id):
    if request.method == "POST":
        item_to_watchlist = AuctionListing.objects.get(id=id)
        remove_watchlist = Watchlist.objects.filter(user = request.user, item = item_to_watchlist)
        remove_watchlist.delete()

        return HttpResponseRedirect(reverse("listing", args=(id,)))


@login_required
def watchlist(request):
    watchlisted_items = Watchlist.objects.filter(user=request.user)

    return render(request, "auctions/watchlist.html", {
        "listings": watchlisted_items
    })


@login_required
def close_listing(request, id):
    if request.method == "POST":
        listing_to_close = AuctionListing.objects.get(id=id)
        listing_to_close.closed = True
        listing_to_close.save()

        return HttpResponseRedirect(reverse("listing", args=(id,)))
