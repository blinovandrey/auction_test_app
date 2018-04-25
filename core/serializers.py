import json

from django.contrib.auth.models import User
from rest_framework import serializers

from core.models import *


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email',)

    def create(self, data):
        user = User.objects.create_user(**data)
        return user


class BetSerializer(serializers.ModelSerializer):

	class Meta:
		model = Bet
		fields = '__all__'
		

class AuctionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Auction
        fields = '__all__'
        readonly_fields = ('user', 'current_max_bet')
    