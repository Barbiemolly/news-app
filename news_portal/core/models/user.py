from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model with role-based logic and subscription relationships.

    Roles:
        - Reader: can view articles and subscribe to publishers/journalists
        - Journalist: can submit/edit articles and newsletters
        - Editor: can approve, reject, and manage articles and newsletters
    """

    ROLE_CHOICES = [
        ("reader", "Reader"),
        ("journalist", "Journalist"),
        ("editor", "Editor"),
        ("publisher", "Publisher"),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="reader")

    # Reader: subscriptions
    subscribed_journalists = models.ManyToManyField(
        "self",
        symmetrical=False,
        related_name="journalist_followers",
        blank=True,
        help_text="Journalists this reader subscribes to",
    )
    subscribed_publishers = models.ManyToManyField(
        "Publisher",
        related_name="reader_subscribers",
        blank=True,
        help_text="Publishers this reader subscribes to",
    )
    bookmarked_articles = models.ManyToManyField(
        "core.Article", blank=True, related_name="bookmarked_by"
    )

    def save(self, *args, **kwargs):
        """
        Prevents reader-only subscriptions from being used by journalists.
        Only clears M2M subscriptions *after* instance has been saved.
        """
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if not is_new and self.role == "journalist":
            self.subscribed_journalists.clear()
            self.subscribed_publishers.clear()

    def __str__(self):
        return f"{self.username} ({self.role})"
