from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from . import forms
from .models import User, Listing, WatchList, Bids, Comment
from django.contrib.auth.decorators import login_required

def index(request):

    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
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

# Displays form, and saves it into the DB if valid
def upload_listing(request):
    form = forms.UploadForm()

    if request.method == 'POST':
        form = forms.UploadForm(request.POST)
        if form.is_valid():
            form.save()

            instance = Listing.objects.get(title = form.cleaned_data["title"])
            instance.user_id = request.user.id
            instance.save()

            return redirect('index')
    return render(request, 'auctions/upload_listing.html', {'form':form})

# MISSING: 
# missing error if the input less money than current bid

def display_listing(request, listing_id):

    id = listing_id
    if request.method == 'POST':  
        form = forms.BidsForm(request.POST)
        if form.is_valid():
            bid = request.POST["current_bid"]
            try:    
                # could simplify this code i guess but i really dont want to bother
                current_bid = Bids.objects.get(listing_id = id).current_bid
                if int(bid) > int(current_bid):
                    instance = Bids.objects.get(listing_id = id)
                    instance.user_id = request.user.id
                    instance.current_bid = bid
                    instance.save()

                    # made this whole mess so I dont can have the price 
                    # displayed at index nice and easy
                    newInstance = Listing.objects.get(id = listing_id)
                    newInstance.starting_bid = bid
                    newInstance.save()

                    return redirect(f"/{listing_id}")
                else:
                    # TODO: return error
                    return redirect(f"/{listing_id}") 
                
            except Bids.DoesNotExist:
                starting_bid = Listing.objects.get(id = listing_id).starting_bid
                if int(bid) > starting_bid:
                    id = listing_id
                    newBid = Bids.objects.create(user_id = request.user.id, listing_id = id, current_bid = bid)
                    newBid.save()
                    return redirect(f"/{listing_id}")
                else:
                    # TODO: return error
                    return redirect(f"/{listing_id}")  
  
    listing = Listing.objects.get(id=listing_id)
    try: 
        user = User.objects.get(id=request.user.id)
    except User.DoesNotExist:
        user = "no"

    delete_listing = ""
    
    try:
        Listing.objects.get(user_id = request.user.id, id = listing_id)
        delete_listing = "True"
    except Listing.DoesNotExist:
        delete_listing = ""
        
    if user != "no":
        try:
            watchlist = WatchList.objects.get(listing_id = listing, user_id = user)
        except WatchList.DoesNotExist:
            watchlist = None
    else:
        watchlist = ""

    try:
        current_bid = Bids.objects.get(listing_id = id).current_bid
    except Bids.DoesNotExist:
        current_bid = Listing.objects.get(id = listing_id).starting_bid

    comments = Comment.objects.filter(listing_id = id)
    

        
    return render(request, "auctions/listing.html", {
        "listing" : listing,
        "watchlist": watchlist,
        "bid": forms.BidsForm(),
        "currentbid": current_bid,
        "comment": forms.CommentForm(),
        "comments": comments,
        "delete_listing": delete_listing,
        "username": request.user.username
    })

# Function to add into watchlist
def watchlist_add(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    user = User.objects.get(id=request.user.id)
    
    createWatchlistObject = WatchList.objects.create(user_id=user, listing_id=listing)
    createWatchlistObject.save()
    
    return redirect(f"/{listing_id}")

# Function to delete from watchlist
def watchlist_delete(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    user = User.objects.get(id=request.user.id)

    instance = WatchList.objects.get(listing_id = listing, user_id = user)
    instance.delete()

    return redirect(f"/{listing_id}")

# Function to publish comment
def publish_comment(request, listing_id):
    if request.method == "POST":
        form = forms.CommentForm(request.POST)
        if form.is_valid():
            id = listing_id
            newComment = Comment.objects.create(user_id = request.user.id, listing_id = id, comment = form.cleaned_data.get("comment"))
            newComment.save()
        
        return redirect(f"/{listing_id}")

# Function to render page of search by categories
def categories(request):
    list_of_categories = ["Fashion","Toys","Electronics",
    "Furniture","Home","Gaming"]
    return render (request, "auctions/categories.html",{
        "categories": list_of_categories    
    })
    
def category_especific(request, category):
    try:
        category_search = Listing.objects.filter(choice = category.upper())      
    except Listing.DoesNotExist:
        category_search = ""

    print(category_search)

    return render(request, "auctions/categories_search.html",{
        "list": category_search,
        "category": category.lower()
    })

# TODO: render page of all the 
def watchlist(request):
    try:
        watchlist_list = WatchList.objects.filter(user_id = request.user.id)
        # This reuturns a list of object that have been added by user
        list = []
        for item in watchlist_list:
            list.append(item.listing_id)
    except Listing.DoesNotExist:
        watchlist_list = ""


    # TODO: using the listing_id in the query
    # <QuerySet [<WatchList: WatchList object (1)>]>

    print(list)
    return render(request, "auctions/watchlist.html",{
        "watchlist": list
    })

# Allows the user if he is the creator of the listing to delete
# the listing
def close_listing(request, listing_id):

    instance = Listing.objects.get(id = listing_id)
    instance.delete()
    return redirect('index')