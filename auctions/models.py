from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator

class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64, unique=True)
    text_description = models.TextField(max_length=256)
    starting_bid = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    user_id = models.IntegerField(default=0)
    CATEGORY_CHOICES = (
        ("FASHION", "Fashion"), 
        ("TOYS", "Toys"),
        ("ELECTRONICS","Electronics"),
        ("HOME","Home"),
        ("FURNITURE", "Furniture"),
        ("GAMING","Gaming")
    )
    # Optional
    imageUrl = models.URLField(max_length=10000, blank=True)
    choice = models.CharField(max_length=11, choices=CATEGORY_CHOICES,
    blank=True)
    
class WatchList(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_id")
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_id", unique=True)

# TODO: MISSING
# If the user created the model have option to delete it(
# relatively simple) Will need to add a user_id atribute 
# to the listing model. 

# Watchlist render function

# Check everything works as implemented !!!!!

class Bids(models.Model):
    current_bid = models.PositiveIntegerField(validators=[MinValueValidator(1)]) 
    listing_id = models.IntegerField(unique=True)
    user_id = models.IntegerField()

class Comment(models.Model):
    comment = models.TextField(max_length=512)
    user_id = models.IntegerField()
    listing_id = models.IntegerField()
    creation_time = models.TimeField(auto_now_add=True)
