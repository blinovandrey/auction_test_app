from django.db import models


# Create your models here.
class Auction(models.Model):
	user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
	description = models.TextField()
	price_start = models.DecimalField(max_digits=10, decimal_places=2)
	price_step = models.DecimalField(max_digits=10, decimal_places=2)
	end_at = models.DateTimeField()
	current_max_bet = models.DecimalField(max_digits=10, decimal_places=2)

	def __str__(self):
		return self.description

	def save(self):
		if not self.current_max_bet:
			self.current_max_bet = self.price_start
		return super(Auction, self).save(*args, **kwargs)

	def update_max_bet(self, bet):
		self.current_max_bet = bet
		self.save()


class Bet(models.Model):
	user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
	auction = models.ForeignKey('core.Auction', on_delete=models.CASCADE)
	value = models.DecimalField(max_digits=10, decimal_places=2)

	def __str__(self):
		return self.value
