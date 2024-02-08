from django.contrib import admin
from .models import User, Category, Auction, Bid, Watchlist, Comment

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username")

class BidAdmin(admin.ModelAdmin):
    list_display = ("bid", "user")

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Category)
admin.site.register(Auction)
admin.site.register(Bid, BidAdmin)
admin.site.register(Watchlist)
admin.site.register(Comment)