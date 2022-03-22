from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    category = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.category}"


class Listing(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="listing_user"
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="listing_category"
    )
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    startBid = models.IntegerField(null=True)
    currentBid = models.IntegerField(default=0)
    imageURL = models.TextField(blank=True)
    status_closed = models.BooleanField(default="False")
    status_listed = models.BooleanField(default="False")
    mine = models.BooleanField(default="False")
    winner = models.CharField(max_length=255, default="", blank=True)
    winnerStatus = models.BooleanField(default="False")
    created_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return f"{self.user} created {self.title} at start-bid ({self.startBid} won)"


class Bid(models.Model):
    listings = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="list")
    participant = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    bid = models.IntegerField(null=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return f"{self.participant} placed ({self.bid} won) in {self.listings}"


class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watch_user")
    watchListings = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="watch_list"
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="watch_list_category"
    )
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    status_listed = models.BooleanField(default="False")

    def __str__(self):
        return f"{self.user} listed ({self.watchListings}) as watchlist"


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comment_user"
    )
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="comment_list"
    )
    comment = models.TextField(max_length=500)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return f"{self.author} commented {self.comment} in {self.listing}"
