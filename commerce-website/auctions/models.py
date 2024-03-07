from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=64, primary_key=True)

    def __str__(self):
        return f"{self.name}"


# не очень понимаю захуя мне это отдельной моделью и как это связывать с аукционом, типо жто просто чтобы были все все ставки? или что? 
class Bid(models.Model):
    bid = models.DecimalField(max_digits=9, decimal_places=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1, related_name="userBids")
    
    def __str__(self):
        return f"{self.bid} by {self.user}"

class Auction(models.Model):
    title = models.CharField(max_length=120, unique=True)
    description = models.CharField(max_length=500)
    price = models.ManyToManyField(Bid, related_name="bids")
    image = models.URLField(blank=True)
    category = models.ForeignKey(Category, blank=True, on_delete=models.CASCADE, default="Other", related_name="incategory")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=1, related_name="userlistings")
    status = models.BooleanField(default=True)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, default=1, related_name="winnerlistings")
    

    def __str__(self):
        return f"{self.title}"

class Watchlist(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, default=1, related_name="watchlistlisting")
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1, related_name="userWatchlist")

    def __str__(self):
        return f"{self.auction} in {self.user}'s watchlist"
    
class Comment(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, default=1, related_name="auctionComment")
    text = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1, related_name="userComment")
    time = models.DateTimeField()

    def __str__(self):
        return f"Comments for {self.auction}"