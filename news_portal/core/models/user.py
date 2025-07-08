"""
Custom user model for the news portal application.

Extends Django's AbstractUser and adds role-based access and user interaction features.
This model supports subscription relationships between users (readers → journalists/publishers)
and bookmarking of articles.

Classes:
    User: Custom user with additional fields for roles, subscriptions, and bookmarks.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model with role-based logic and subscription relationships.

    Extends:
        django.contrib.auth.models.AbstractUser

    Roles:
        - Reader: Can view articles and subscribe to journalists and publishers.
        - Journalist: Can submit/edit articles and newsletters.
        - Editor: Can approve, reject, and manage articles and newsletters.
        - Publisher: Can manage journalists and publish under a brand.

    Fields:
        role (str): The role assigned to the user.
        subscribed_journalists (User): Readers following journalists.
        subscribed_publishers (Publisher): Readers following publishers.
        bookmarked_articles (Article): Articles bookmarked by the user.
    """

    ROLE_CHOICES = [
        ("reader", "Reader"),
        ("journalist", "Journalist"),
        ("editor", "Editor"),
        ("publisher", "Publisher"),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="reader",
        help_text="The role assigned to the user, determines their permissions."
    )

    subscribed_journalists = models.ManyToManyField(
        "self",
        symmetrical=False,
        related_name="journalist_followers",
        blank=True,
        help_text="Journalists this reader subscribes to.",
    )

    subscribed_publishers = models.ManyToManyField(
        "Publisher",
        related_name="reader_subscribers",
        blank=True,
        help_text="Publishers this reader subscribes to.",
    )

    bookmarked_articles = models.ManyToManyField(
        "core.Article",
        blank=True,
        related_name="bookmarked_by",
        help_text="Articles bookmarked by the user for later reading.",
    )

    def save(self, *args, **kwargs):
        """
        Overrides the save method to enforce subscription rules.

        Journalists cannot subscribe to other journalists or publishers.
        If a user's role is changed to 'journalist', all their subscriptions are cleared.
        """
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if not is_new and self.role == "journalist":
            self.subscribed_journalists.clear()
            self.subscribed_publishers.clear()

    def __str__(self) -> str:
        """
        Returns a string representation of the user including their username and role.

        Returns:
            str: A human-readable string showing the username and role.
        """
        return f"{self.username} ({self.role})"
