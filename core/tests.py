import json
from datetime import datetime
from functools import wraps
from unittest import mock

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient, APITestCase, force_authenticate

from core.models import *


def authenticated_as_admin(func):
    @wraps(func)
    def wrapped(self):
        user = User.objects.get(username='admin')
        self.client.force_authenticate(user=user)
        func(self)
    return wrapped


def authenticated_as_user(func):
    @wraps(func)
    def wrapped(self):
        user = User.objects.get(username='user')
        self.client.force_authenticate(user=user)
        func(self)
    return wrapped


def authenticated_as_another_user(func):
    @wraps(func)
    def wrapped(self):
        user = User.objects.get(username='another_user')
        self.client.force_authenticate(user=user)
        func(self)
    return wrapped


class AuctionCreateTests(APITestCase):
    
    def setUp(self):
        self.client = APIClient()
        if not User.objects.all():
            self.user_admin = User.objects.create_user(
                id=1,
                username="admin",
                first_name="admin",
                password="qwerqwer",
                is_superuser=True
            )
            
    def tearDown(self):
        self.user_admin.delete()

    @authenticated_as_admin
    def test_create_auction(self):
        data = {
            "description": "test",
            "price_start": "100.00",
            "price_step": "10.00",
            "end_at": "2018-04-26T18:25:43.511Z"
        }
        response = self.client.post('/api/auctions/', data)
        self.assertEqual(response.status_code, 201)


class BetCreateTests(APITestCase):
    
    def setUp(self):
        self.client = APIClient()

        self.user_admin = User.objects.create_user(
            username="admin",
            first_name="admin",
            password="qwerqwer",
            is_superuser=True
        )

        self.user = User.objects.create_user(
            username="user",
            first_name="user",
            password="qwerqwer",
            is_superuser=True
        )

        self.another_user = User.objects.create_user(
            username="another_user",
            first_name="another_user",
            password="qwerqwer",
            is_superuser=True
        )

        self.auction = Auction.objects.create(
            user=self.user,
            description="test auction",
            price_start="200.00",
            price_step="20.00",
            end_at=datetime.now()
        )

    def tearDown(self):
        self.user_admin.delete()
        self.user.delete()
        self.auction.delete()

    @authenticated_as_user
    def test_self_auction_bet(self):
        data = {
            'auction': self.auction.id,
            'value': 220
        }
        response = self.client.post('/api/bets/', data)
        self.assertEqual(response.status_code, 403)

    @authenticated_as_admin
    def test_auction_bet(self):
        data = {
            'auction': self.auction.id,
            'value': 220
        }
        response = self.client.post('/api/bets/', data)
        self.assertEqual(response.status_code, 201)

    @authenticated_as_admin
    def test_auction_wrong_bet(self):
        data = {
            'auction': self.auction.id,
            'value': 215
        }
        response = self.client.post('/api/bets/', data)
        self.assertEqual(response.status_code, 400)

    @authenticated_as_another_user
    def test_auction_bet(self):
        data = {
            'auction': self.auction.id,
            'value': 240
        }
        response = self.client.post('/api/bets/', data)
        self.assertEqual(response.status_code, 201)
