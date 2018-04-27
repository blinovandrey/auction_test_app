import logging

import celery
from django.contrib.auth.models import User
from django.core.mail import send_mass_mail

from core.models import Auction


@celery.task
def send_auction_finished_notification_email(user_id, auction_id):
    try:
        user = User.objects.get(pk=user_id)
        auction = Auction.objects.get(pk=auction_id)
        auction.is_finished = True
        auction.save()
        emails = list(auction.bet_set.values_list("user__email", flat=True).distinct())
        winner = auction.current_max_bet.user if auction.current_max_bet else None
        mail_tuple = ("Auction has been finished",
            f"Auction {auction.description} has been finished! \
            	Winner is {winner.get_full_name() if winner else ''} \
            	with a bet of {auction.current_max_bet or ''}",
            "from@example.com",
            emails,)
        send_mass_mail((mail_tuple,))
    except (User.DoesNotExist, Auction.DoesNotExist):
        logging.warning(f"User or Auction was not found")
