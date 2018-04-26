from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import Auction
from core.tasks import send_auction_finished_notification_email

@receiver(post_save, sender=Auction)
def create_email_send_task(sender, instance, created, **kwargs):
	if created:
		args = (instance.user.id, instance.id,)
		send_auction_finished_notification_email.apply_async(args, eta=instance.end_at)