from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return f"{self.username} {self.email}"

class AuctionListing(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=512)
    starting_bid = models.IntegerField()
    image = models.URLField()
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ListingSeller")
    
    class Category(models.TextChoices):
        Fashion = 'Fashion'
        Toys = 'Toys'
        Electronics = 'Electronics'
        Home = 'Home'
        Sports = 'Sporting Goods'
        Vehicles = 'Vehicles'

    categories = models.CharField(max_length=16, choices=Category.choices, blank = True)

    def __str__(self):
        return f"{self.name} {self.description} {self.starting_bid} Seller: {self.seller}"
    

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Buyer")
    item = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="Listing")
    bid_amount = models.IntegerField()

    def __str__(self):
        return f"{self.user} {self.item} {self.bid_amount}"

class Comment(models.Model):
    comment = models.CharField(max_length=256)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Commenter")
    item = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="ListComment")

    def __str__(self):
        return f"{self.user} {self.item} {self.comment}"


