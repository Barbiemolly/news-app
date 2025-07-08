from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models.article import Article
from django.core.mail import send_mail
from django.conf import settings


@receiver(post_save, sender=Article)
def send_approval_email(sender, instance, created, **kwargs):
    if not created and instance.status == "approved" and instance.approved_at:
        # Send to subscribers of either the publisher or journalist
        subscribers = set()

        if instance.publisher:
            for reader in instance.publisher.reader_subscribers.all():
                subscribers.add(reader.email)

        for reader in instance.author.journalist_followers.all():
            subscribers.add(reader.email)

        if subscribers:
            send_mail(
                subject=f"New Article Published: {instance.title}",
                message=f"Check out the newly approved article by {instance.author.username}.\n\n{instance.content[:200]}...",
                from_email="no-reply@newspot.com",
                recipient_list=list(subscribers),
                fail_silently=True,
            )


@receiver(post_save, sender=Article)
def notify_subscribers_on_approval(sender, instance, **kwargs):
    if instance.status == "approved" and instance.approved_at:
        publisher_subs = (
            instance.publisher.subscribers.all() if instance.publisher else []
        )
        journalist_subs = instance.author.followers.all()
        recipients = set(
            user.email for user in (publisher_subs | journalist_subs) if user.email
        )

        subject = f"New article published: {instance.title}"
        message = f"{instance.author.username} just published a new article: {instance.title}\n\nRead it now on News Portal!"
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, list(recipients))
