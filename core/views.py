from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import mixins, viewsets
from core.permissions import IsNotBetAuctionOwner
from core.serializers import *
from core.mixins import BetValidateMixin, AuctionCreateMixin
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class UserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AuctionViewSet(AuctionCreateMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
	queryset = Auction.objects.all()
	serializer_class = AuctionSerializer
	permission_classes = (IsAuthenticated,)


class BetViewSet(BetValidateMixin, viewsets.GenericViewSet):
	queryset = Bet.objects.all()
	serializer_class = BetSerializer
	permission_classes = (IsAuthenticated, IsNotBetAuctionOwner)
