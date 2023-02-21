from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm, Textarea,TextInput, NumberInput
from .models import User, Listing, Bid, Comment
class NewCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        labels = {
            'comment' : ''
        }
        widgets = {
            'comment' : Textarea(attrs ={'cols' : 50, 'rows' : 3, 'placeholder': "Write a comment..."})
        }
class NewBidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['price']
        labels = {
            'price' : ''
        }
        widgets = {
            'price':  NumberInput()
        }
class NewListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'StartingBid', 'category', 'image']
        labels = {
            "StartingBid" : '',
            'title' :'',
            'description': '',
            'image' : ''
        }
        widgets= {
            "title" : TextInput(attrs={'placeholder': "Name of the product"}),
            "description" : Textarea(attrs={'cols': 80, 'rows': 10, 'placeholder' : 'Write a description here'},),
            "StartingBid" : NumberInput(attrs={'placeholder': "Starting bid"})
        }
def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "listings" : listings
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


def createListing(request):
    if request.method == "GET":
        form = NewListingForm()
        return render(request, "auctions/ListingCreate.html",{
            "form": form
        })
    else:
        form = NewListingForm(request.POST, request.FILES)
        listings = Listing.objects.all()
        TITLES = []
        for listing in listings:
            TITLES.append(listing.title)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.creator = request.user
            if listing.title in TITLES:
                return render(request, "auctions/ListingCreate.html", {
                    "form" : NewListingForm,
                    "exists" : True
                })
            else:
                listing.save()
                return HttpResponseRedirect(reverse("listing", args=[listing]))

def listing(request, listing):
    if request.method == "GET":
        listings = Listing.objects.all()
        for list in listings:
            if list.title == listing:
                listing = list
        if listing.bid:
            bid = listing.bid
        else:
            bid = listing.StartingBid
        user = request.user
        if user in listing.watching.all():
            inside = True
        else:
            inside = False
        form = NewBidForm()
        comments = Comment.objects.filter(auction=listing)
        return render(request, "auctions/listing.html", {
            "listing" : listing,
            "bid" : bid,
            "bidNumber": listing.bidNumber,
            "form" : form,
            "watchlist" : inside,
            "user" : request.user,
            "commentform" : NewCommentForm(),
            "comments" : comments
        })

def bid(request, listing):
    form = NewBidForm(request.POST)
    if form.is_valid():
        listing = Listing.objects.get(title=listing)
        bid = form.save(commit=False)
        if valid(bid.price, listing):
            bid.user = request.user
            bid.auction = listing
            bid.save()
            listing.bidNumber = listing.bidNumber + 1
            listing.bid = bid.price
            listing.save()
            return HttpResponseRedirect(reverse("listing", args=[listing]))
        else:
            user = request.user
            if user in listing.watching.all():
                inside = True
            else:
                inside = False
            comments = Comment.objects.filter(auction=listing)

            return render(request, "auctions/listing.html", {
                "listing" : listing,
                "bidNumber" : listing.bidNumber,
                "form" : NewBidForm(),
                "min_value" : True,
                "watchlist" : inside,
                "user" : request.user,
                "commentform": NewCommentForm(),
                "comments" : comments
            })

def valid(bid, listing):
    if listing.bid:
        if bid <= listing.bid:
            return False
        else:
            return True
    else:
        if bid <= listing.StartingBid:
            return False
        else:
            return True


def alter_watchlist(request, listing):
    if request.method == "POST":
        listing = Listing.objects.get(title = listing)
        user = request.user
        if user not in listing.watching.all():
            listing.watching.add(user)
        else:
            listing.watching.remove(user)
        return HttpResponseRedirect(reverse("listing", args=[listing]))

def watchlist(request):
        return render(request, "auctions/watchlist.html", {
            "listings" : Listing.objects.all(),
            "user" : request.user,
        })

def close_listing(request, listing):
        listing = Listing.objects.get(title=listing)
        if request.POST:
            if listing.bid:
                listing.closed = True
                highestbid = listing.bid
                winner = Bid.objects.get(auction=listing, price=highestbid)
                listing.winner = winner.user
                listing.save()
                return HttpResponseRedirect(reverse("listing", args=[listing]))
            else:
                user = request.user
                if user in listing.watching.all():
                    inside = True
                else:
                    inside = False
                return render(request, "auctions/listing.html", {
                    "listing" : listing,
                    "watchlist" : inside,
                    "bidNumber" : listing.bidNumber,
                    "form" : NewBidForm(),
                    "user" : request.user,
                    "commentform": NewCommentForm(),
                    "error_closing" : True

                })

def comment(request, listing):
        listing = Listing.objects.get(title=listing)
        form = NewCommentForm(request.POST)
        comment = form.save(commit=False)
        comment.user = request.user
        comment.auction = listing
        comment.save()
        return HttpResponseRedirect(reverse("listing", args=[listing]))

def categories(request):
    if request.method == "GET":
        categories = Listing.objects.values('category')
        CATEGORIES = [
            "Antiques", "Electronics", "Machinery", "Fashion", "Home", "Sports", "Retail", "Toys", "Tools", "Vehicles", "Recreation"
        ]
        return render(request, "auctions/categories.html", {
            "categories" : CATEGORIES
        })
    else:
        CATEGORIES = [
            "Antiques", "Electronics", "Machinery", "Fashion", "Home", "Sports", "Retail", "Toys", "Tools", "Vehicles", "Recreation"
        ]
        categoryy = request.POST['category']
        listings = Listing.objects.filter(category = categoryy)
        return render(request, "auctions/categories.html", {
            "categories" : CATEGORIES,
            "listings" : listings,
            "categorySelected" : categoryy
        })










