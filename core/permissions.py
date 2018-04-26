from rest_framework import permissions
from core.models import Auction

class IsNotBetAuctionOwner(permissions.BasePermission):
    
    def has_permission(self, request, view):
        try:
            auction = Auction.objects.get(pk=request.data.get('auction'))
        except Auction.DoesNotExist:
            return False
        else: 
            return auction.user != request.user
