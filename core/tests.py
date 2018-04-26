from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework.test import force_authenticate
from unittest import mock
from functools import wraps
from django.contrib.auth.models import User
import json
from datetime import datetime

from core.models import *


def authenticated_as_admin(func):
    @wraps(func)
    def wrapped(self):
        user = User.objects.get(username='admin')
        self.client.force_authenticate(user=user)
        func(self)
    return wrapped


def authenticated_as_other(func):
    @wraps(func)
    def wrapped(self):
        user = User.objects.get(username='other')
        self.client.force_authenticate(user=user)
        func(self)
    return wrapped


class CoreTests(APITestCase):
    
    def setUp(self):
        self.client = APIClient()
        if not User.objects.all():
            User.objects.create_user(
                id=1,
                username="admin",
                first_name="admin",
                password="qwerqwer",
                is_superuser=True
            )
            User.objects.create_user(
                id=2,
                username="other",
                first_name="other",
                password="qwerqwer",
                is_superuser=True
            )
        if not Auction.objects.all():
            Auction.objects.create(
                id=1,
                user_id=1,
                description="test",
                price_start="100.00",
                price_step="10.00",
                end_at=datetime.now()
            )
            Auction.objects.create(
                id=2,
                user_id=2,
                description="test_other",
                price_start="200.00",
                price_step="20.00",
                end_at=datetime.now()
            )


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


    @authenticated_as_other
    def test_create_auction_by_other_user(self):
        data = {
            "description": "test",
            "price_start": "200.00",
            "price_step": "20.00",
            "end_at": "2018-04-26T18:25:43.511Z"
        }
        response = self.client.post('/api/auctions/', data)
        self.assertEqual(response.status_code, 201)


    @authenticated_as_admin
    def test_self_auction_bet(self):
        data = {
            'auction': 1,
            'value': 110
        }
        response = self.client.post('/api/bets/', data)
        self.assertEqual(response.status_code, 403)


    @authenticated_as_admin
    def test_other_auction_bet(self):
        data = {
            'auction': 2,
            'value': 220
        }
        response = self.client.post('/api/bets/', data)
        self.assertEqual(response.status_code, 201)