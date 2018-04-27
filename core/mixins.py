from rest_framework import mixins, status
from rest_framework.response import Response

from core.models import Auction


class BetValidateMixin(mixins.CreateModelMixin):

	def create(self, request, *args, **kwargs):
		request.data['user'] = request.user.id
		value = request.data.get('value') or 0
		try:
			auction = Auction.objects.get(pk=request.data.get('auction'))
		except Auction.DoesNotExist:
			return Response('Auction does not exist', status=status.HTTP_400_BAD_REQUEST)
		
		if auction.is_finished:
			return Response('Auction has been finished', status=status.HTTP_400_BAD_REQUEST)
		
		if not auction.is_correct_bet(value):
			return Response('Enter a value greater than current bet or multiple by step', status=status.HTTP_400_BAD_REQUEST)
		
		return mixins.CreateModelMixin.create(self, request, *args, **kwargs)			


class AuctionCreateMixin(mixins.CreateModelMixin):

	def create(self, request, *args, **kwargs):
		request.data.update({'user': request.user.id})
		return mixins.CreateModelMixin.create(self, request, *args, **kwargs)
