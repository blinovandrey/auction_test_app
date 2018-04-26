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
        data['is_superuser'] = True
        user = User.objects.create_user(**data)
        return user


class BetSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    
    def get_user_name(self, obj):
        return obj.user.get_full_name()

    class Meta:
        model = Bet
        fields = ('auction', 'user', 'value', 'user_name')
        

class AuctionSerializer(serializers.ModelSerializer):
    bets = BetSerializer(many=True, read_only=True, source='bet_set')
    
    class Meta:
        model = Auction
        fields = '__all__'
        read_only_fields = ('current_max_bet',)
    