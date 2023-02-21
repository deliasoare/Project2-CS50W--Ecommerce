from django.contrib.auth.models import AbstractUser
from django.db import models
class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField(auto_now=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="all_creators")
    image = models.ImageField(upload_to = 'static/auctions', default = "static/auctions/notworking.png")
    description = models.CharField(max_length=1000)
    StartingBid = models.FloatField()
    bid = models.FloatField(blank=True, null=True)
    bidNumber=models.IntegerField( default = 0 )
    watching = models.ManyToManyField(User, related_name="watchers")
    winner = models.ForeignKey(User, on_delete = models.CASCADE, null=True)
    closed = models.BooleanField(default = False)
    class categories(models.TextChoices):
        ANTIQUES = "Antiques"
        ELECTRONICS = "Electronics"
        MACHINERY = "Machinery"
        FASHION = "Fashion"
        HOME = "Home"
        SPORTS = "Sports"
        RETAIL = "Retail"
        TOYS = "Toys"
        TOOLS = "Tools"
        VEHICLES = "Vehicles"
        RECREATION = "Recreation"

    category = models.CharField(
        max_length = 11,
        choices = categories.choices
    )
    def __str__(self):
        return self.title

class Bid(models.Model):
    auction = models.ForeignKey(Listing, on_delete=models.PROTECT, related_name="listing")
    price = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="all_bidders")


class Comment(models.Model):
    auction = models.ForeignKey(Listing, on_delete=models.PROTECT)
    comment = models.CharField(max_length=150)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="all_commenters")
    date = models.DateField(auto_now=True)



