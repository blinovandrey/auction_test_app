from datetime import datetime
from decimal import Decimal

from django.db import models


# Create your models here.
class Auction(models.Model):
	user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
	description = models.TextField()
	price_start = models.DecimalField(max_digits=10, decimal_places=2)
	price_step = models.DecimalField(max_digits=10, decimal_places=2)
	end_at = models.DateTimeField()
	current_max_bet = models.OneToOneField('core.Bet', related_name='current_max_bet', null=True, on_delete=models.CASCADE)
	is_finished = models.BooleanField(default=False)

	def __str__(self):
		return self.description

	def is_correct_bet(self, value):
		current_bet = self.current_max_bet.value if self.current_max_bet else self.price_start
		return Decimal(value) > current_bet and Decimal(value) % self.price_step == 0


class Bet(models.Model):
	user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
	auction = models.ForeignKey('core.Auction', on_delete=models.CASCADE)
	value = models.DecimalField(max_digits=10, decimal_places=2)

	def __str__(self):
		return str(self.value)

	def save(self, *args, **kwargs):
		super(Bet, self).save(*args, **kwargs)
		self.auction.current_max_bet = self
		self.auction.save()
		return self
