from rest_framework import mixins
from core.models import Auction
from rest_framework.response import Response
from rest_framework import status

class BetValidateMixin(mixins.CreateModelMixin):

	def create(self, request, *args, **kwargs):
		request.data['user'] = request.user.id
		value = request.data.get('value') or 0
		auction = Auction.objects.get(pk=request.data.get('auction'))
		if not auction.is_correct_bet(value):
			return Response('Введите значение больше текущей ставки или кратное шагу аукциона', status=status.HTTP_400_BAD_REQUEST)
		else:
			return mixins.CreateModelMixin.create(self, request, *args, **kwargs)			


class AuctionCreateMixin(mixins.CreateModelMixin):

	def create(self, request, *args, **kwargs):
		request.data['user'] = request.user.id
		return mixins.CreateModelMixin.create(self, request, *args, **kwargs)