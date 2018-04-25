from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import mixins, viewsets

from core.serializers import *


# Create your views here.
class UserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
