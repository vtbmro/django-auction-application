from django.contrib import admin
from .models import Listing, User, WatchList, Bids, Comment

# Register your models here.
admin.site.register(Listing)
admin.site.register(User)
admin.site.register(WatchList)
admin.site.register(Bids)
admin.site.register(Comment)