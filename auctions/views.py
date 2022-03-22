from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Category, Listing, Bid, WatchList, Comment


def index(request):
    categories = Category.objects.all()
    listings = Listing.objects.all()
    return render(
        request,
        "auctions/index.html",
        {"categories": categories, "listings": listings},
    )


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
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required(login_url="/login")
def create(request):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)

    if request.method == "POST":
        title = request.POST.get("create_title").strip()
        description = request.POST.get("create_description").strip()
        startBid = request.POST.get("create_bid").strip()
        imageURL = request.POST.get("create_image").strip()
        selectedCategory = request.POST.get("create_category").strip()
        category = Category.objects.get(category=selectedCategory)

        if int(startBid) > 10000000:
            return render(
                request,
                "auctions/create.html",
                {
                    "alertMsg": "start bid must under 10,000,000 won!",
                    "title": title,
                    "description": description,
                    "imageURL": imageURL,
                    "categories": Category.objects.all(),
                },
            )

        try:
            listing = Listing(
                user=user,
                title=title,
                description=description,
                startBid=startBid,
                imageURL=imageURL,
                category=category,
            )
            listing.save()
            return redirect("index")
        except:
            return render(
                request,
                "auctions/create.html",
                {
                    "alertMsg": "This title already existed!",
                    "title": title,
                    "description": description,
                    "imageURL": imageURL,
                    "categories": Category.objects.all(),
                },
            )

    return render(
        request,
        "auctions/create.html",
        {
            "categories": Category.objects.all(),
        },
    )


def filtered(request, category):
    category = category
    categories = Category.objects.all()
    filteredCategory = Category.objects.get(category=category)
    listings = Listing.objects.all().filter(category=filteredCategory)
    return render(
        request,
        "auctions/index.html",
        {
            "filteredListings": listings,
            "categories": categories,
        },
    )


@login_required(login_url="/login")
def listing(request, title):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)

    title = title.strip()
    listing = Listing.objects.get(title=title)
    userListing = Listing.objects.all().filter(user=user)
    bids = Bid.objects.all().filter(listings=listing)
    comments = Comment.objects.all().filter(listing=listing)
    commentContent = request.POST.get("comment_area")

    if listing in userListing:
        listing.mine = True
    else:
        listing.mine = False
    mine = listing.mine

    if str(listing.winner) == str(user):
        listing.winnerStatus = True
    else:
        listing.winnerStatus = False
    winnerStatus = listing.winnerStatus

    if request.method == "POST":
        finalBid = Bid.objects.filter(listings=listing).last()
        if "close_list_button" in request.POST:
            if finalBid == None:
                return render(
                    request,
                    "auctions/listing.html",
                    {
                        "alertMsg": "Nobody put bids yet",
                        "listing": listing,
                        "userListing": userListing,
                        "mine": mine,
                        "bids": bids,
                        "comments": comments,
                        "winnerStatus": winnerStatus,
                    },
                )
            else:
                listing.winner = str(finalBid.participant)
                listing.status_closed = True
                listing.save()
                return render(
                    request,
                    "auctions/listing.html",
                    {
                        "listing": listing,
                        "userListing": userListing,
                        "mine": mine,
                        "bids": bids,
                        "comments": comments,
                        "winnerStatus": winnerStatus,
                    },
                )

        if "watch_list_button" in request.POST:
            try:
                watchList = WatchList.objects.get(watchListings=listing)
                watchList.delete()
                listing.status_listed = False
                listing.save()
                return render(
                    request,
                    "auctions/listing.html",
                    {
                        "alertMsg": "This page is already in your watch list!",
                        "listing": listing,
                        "userListing": userListing,
                        "mine": mine,
                        "bids": bids,
                        "comments": comments,
                        "winnerStatus": winnerStatus,
                    },
                )
            except:
                watch = WatchList(
                    user=user,
                    watchListings=listing,
                    status_listed=True,
                    category=listing.category,
                )
                listing.status_listed = True
                watch.save()
                listing.save()
                return render(
                    request,
                    "auctions/listing.html",
                    {
                        "successMsg": "This list is added to your watch list successfully!",
                        "listing": listing,
                        "userListing": userListing,
                        "mine": mine,
                        "bids": bids,
                        "comments": comments,
                        "winnerStatus": winnerStatus,
                    },
                )

        if "comment_submit" in request.POST:
            if commentContent == None or commentContent == "":
                return render(
                    request,
                    "auctions/listing.html",
                    {
                        "commentAlertMsg": "You can't save with empty comment!",
                        "listing": listing,
                        "userListing": userListing,
                        "mine": mine,
                        "bids": bids,
                        "comments": comments,
                        "winnerStatus": winnerStatus,
                    },
                )
            else:
                comment = Comment(
                    author=user,
                    listing=listing,
                    comment=commentContent,
                )
                comment.save()

        currentBid = request.POST.get("current_bid")
        bid = Bid(
            listings=listing,
            participant=user,
            bid=currentBid,
        )

        if "put_bid" in request.POST:
            if currentBid == None or currentBid == "":
                return render(
                    request,
                    "auctions/listing.html",
                    {
                        "listing": listing,
                        "userListing": userListing,
                        "mine": mine,
                        "bids": bids,
                        "comments": comments,
                        "winnerStatus": winnerStatus,
                    },
                )

            if int(currentBid) > 10000000:
                return render(
                    request,
                    "auctions/listing.html",
                    {
                        "alertMsg": "bid must under 10,000,000 won!",
                        "listing": listing,
                        "userListing": userListing,
                        "mine": mine,
                        "bids": bids,
                        "comments": comments,
                        "winnerStatus": winnerStatus,
                    },
                )
            elif int(currentBid) <= int(listing.currentBid):
                return render(
                    request,
                    "auctions/listing.html",
                    {
                        "alertMsg": "bid must greater than current bid!",
                        "listing": listing,
                        "userListing": userListing,
                        "mine": mine,
                        "bids": bids,
                        "comments": comments,
                        "winnerStatus": winnerStatus,
                    },
                )
            elif int(currentBid) <= int(listing.startBid):
                return render(
                    request,
                    "auctions/listing.html",
                    {
                        "alertMsg": "Please put your bid greater than start bid",
                        "listing": listing,
                        "userListing": userListing,
                        "mine": mine,
                        "bids": bids,
                        "comments": comments,
                        "winnerStatus": winnerStatus,
                    },
                )
            else:
                listing.currentBid = currentBid
                bid.save()
                listing.save()
                return render(
                    request,
                    "auctions/listing.html",
                    {
                        "listing": listing,
                        "userListing": userListing,
                        "mine": mine,
                        "bids": bids,
                        "comments": comments,
                        "winnerStatus": winnerStatus,
                    },
                )

    return render(
        request,
        "auctions/listing.html",
        {
            "listing": listing,
            "userListing": userListing,
            "mine": mine,
            "bids": bids,
            "comments": comments,
            "winnerStatus": winnerStatus,
        },
    )


@login_required(login_url="/login")
def watchList(request, username):
    username = username
    if request.user.is_authenticated:
        name = request.user.username
        user = User.objects.get(username=name)

    categories = Category.objects.all()
    watchListings = WatchList.objects.all().filter(user=user)

    if not username == name:
        return render(
            request,
            "auctions/watch_list.html",
            {"alertMsg": "You don't have permission to access this page"},
        )

    return render(
        request,
        "auctions/watch_list.html",
        {"watchListings": watchListings, "categories": categories},
    )


@login_required(login_url="/login")
def filteredWatchList(request, category):
    if request.user.is_authenticated:
        name = request.user.username
        user = User.objects.get(username=name)

    category = category
    categories = Category.objects.all()
    filteredCategory = Category.objects.get(category=category)
    watchListings = WatchList.objects.all().filter(user=user)
    filteredWatchListings = WatchList.objects.all().filter(category=filteredCategory)

    return render(
        request,
        "auctions/watch_list.html",
        {
            "filteredWatchListings": filteredWatchListings,
            "watchListings": watchListings,
        },
    )
