from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class listing(models.Model):

    bid_price = models.DecimalField(max_digits=5, decimal_places=2)
    title = models.CharField(name="title", max_length=250)
    description = models.CharField(name="description", max_length= 700)
    category = models.CharField(name="category", max_length=20, default="Not Specified")
    current_price = models.DecimalField(max_digits=5, decimal_places=2)
    slug = models.SlugField(name="slug")
    image = models.ImageField(upload_to='auctions/media/', null=True)
    status = models.BooleanField(default=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default=User)

class comments(models.Model):
    listing_id = models.ForeignKey(listing, on_delete=models.CASCADE, default=listing)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default=User)
    # _hash 
    comment = models.CharField(max_length=250, blank=False)
    #order  = models.IntegerField(default=0)
    #level = models.IntegerField(default=0)

class bids(models.Model):
    listing_id = models.ForeignKey(listing, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=User)
    value = models.IntegerField(default=0)


class watch_list(models.Model):

    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default=User )
    listing_id = models.ForeignKey(listing, on_delete=models.CASCADE, default=listing)

    class Meta:
        unique_together = ['user_id', 'listing_id']

 