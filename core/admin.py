from django.contrib import admin

from core.models import *


# Register your models here.
@admin.register(Auction)
class AuctionAdmin(admin.ModelAdmin):
	pass

@admin.register(Bet)
class BetAdmin(admin.ModelAdmin):
	pass
