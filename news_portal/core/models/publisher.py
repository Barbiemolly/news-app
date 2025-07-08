"""
Defines the Publisher model for the news portal application.

A publisher is an entity that owns and manages content published by assigned
journalists and editors. Each publisher is owned by a single user with the role "publisher".
"""

from django.db import models
from django.db.models import PROTECT
from core.models.user import User


class Publisher(models.Model):
    """
    Represents a publisher organization or media brand.

    Publishers are associated with a single owner (user with role 'publisher'),
    and can have multiple assigned editors and journalists.

    Fields:
        name (str): The publisher's name.
        description (str): Optional description or about section.
        owner (User): The user account that owns this publisher (must have role 'publisher').

    Relationships:
        editors (User): Users with role 'editor' assigned to moderate this publisher's content.
        journalists (User): Users with role 'journalist' who submit articles under this publisher.
    """

    name = models.CharField(
        max_length=255,
        help_text="Name of the publisher."
    )

    description = models.TextField(
        blank=True,
        help_text="Optional description or bio of the publisher."
    )

    editors = models.ManyToManyField(
        User,
        related_name="publisher_editors",
        limit_choices_to={"role": "editor"},
        help_text="Editors assigned to this publisher.",
    )

    journalists = models.ManyToManyField(
        User,
        related_name="publisher_journalists",
        limit_choices_to={"role": "journalist"},
        help_text="Journalists who write under this publisher.",
    )

    owner = models.OneToOneField(
        User,
        on_delete=PROTECT,
        related_name="publisher_profile",
        limit_choices_to={"role": "publisher"},
        help_text="User who owns this publisher profile (must have role 'publisher').",
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        """
        Returns a string representation of the publisher.

        Returns:
            str: The name of the publisher.
        """
        return self.name
