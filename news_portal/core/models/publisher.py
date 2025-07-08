from django.db import models
from core.models.user import User
from django.db.models import PROTECT


class Publisher(models.Model):
    """
    Represents a publisher entity.
    Journalists can publish under it; editors manage its content.
    """

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    editors = models.ManyToManyField(
        User,
        related_name="publisher_editors",
        limit_choices_to={"role": "editor"},
        help_text="Editors assigned to this publisher",
    )
    journalists = models.ManyToManyField(
        User,
        related_name="publisher_journalists",
        limit_choices_to={"role": "journalist"},
        help_text="Journalists who write under this publisher",
    )
    from django.db.models import PROTECT

    owner = models.OneToOneField(
        User,
        on_delete=PROTECT,
        related_name="publisher_profile",
        limit_choices_to={"role": "publisher"},
        help_text="User who owns this publisher profile",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name
