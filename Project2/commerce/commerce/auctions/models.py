from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"

class AuctionListing(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=512)
    starting_bid = models.DecimalField(decimal_places=2, max_digits=8)
    image = models.URLField(blank = True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ListingSeller")
    created_at = models.DateTimeField(auto_now_add=True)
    closed = models.BooleanField(default=False)
    
    class Category(models.TextChoices):
        Fashion = 'Fashion'
        Toys = 'Toys'
        Electronics = 'Electronics'
        Home = 'Home'
        Sports = 'Sporting Goods'
        Vehicles = 'Vehicles'

    categories = models.CharField(max_length=16, choices=Category.choices, blank = True)
    # categories = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name="Categories")

    def __str__(self):
        return f"{self.name} {self.description} {self.starting_bid} Seller: {self.seller}"
    

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Buyer")
    item = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="Listing")
    bid_amount = models.DecimalField(decimal_places=2, max_digits=8)

    def __str__(self):
        return f"{self.user} {self.item} {self.bid_amount}"

class Comment(models.Model):
    comment = models.CharField(max_length=256)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Commenter")
    item = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="ListComment")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} {self.item} {self.comment}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Watchlister")
    item = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="WatchlistedListing")

    def __str__(self):
        return f"{self.user} {self.item}"
