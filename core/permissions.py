from rest_framework import permissions

class IsNotBetAuctionOwner(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        return obj.auction.user != request.user
