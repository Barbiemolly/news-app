"""
Defines the Newsletter model for the news portal application.

Newsletters are submitted by journalists and reviewed by editors.
This model supports workflow transitions (submit → approve/reject),
soft deletion, and reason tracking for rejections.
"""

from django.db import models
from django.utils import timezone
from core.models.user import User


class Newsletter(models.Model):
    """
    Represents a newsletter submitted by a journalist.

    Newsletters follow a submission and editorial review process similar to articles.
    Editors can approve, reject with a reason, or soft-delete newsletters.

    Fields:
        title (str): The title of the newsletter.
        content (str): Full newsletter content.
        created_at (datetime): When the newsletter was created.
        updated_at (datetime): When it was last updated.
        approved_at (datetime): When the newsletter was approved.
        status (str): Editorial status ('submitted', 'approved', 'rejected').
        rejection_reason (str): Reason provided by the editor if rejected.
        is_deleted (bool): Indicates soft deletion.
        deleted_at (datetime): Timestamp of when soft-deleted.
        author (User): The journalist who created the newsletter.
    """

    STATUS_CHOICES = [
        ("submitted", "Submitted"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    title = models.CharField(
        max_length=255,
        help_text="The newsletter's title."
    )

    content = models.TextField(
        help_text="The full body content of the newsletter."
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the newsletter was created."
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp of the last update to the newsletter."
    )

    approved_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Timestamp when the newsletter was approved."
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="submitted",
        help_text="Current editorial status of the newsletter.",
    )

    rejection_reason = models.TextField(
        blank=True,
        null=True,
        help_text="Optional reason provided by the editor for rejection."
    )

    is_deleted = models.BooleanField(
        default=False,
        help_text="Soft delete flag. When True, the newsletter is hidden but not removed from DB."
    )

    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Timestamp when the newsletter was soft deleted."
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="newsletters",
        limit_choices_to={"role": "journalist"},
        help_text="The journalist who authored the newsletter."
    )

    def soft_delete(self):
        """
        Soft deletes the newsletter without removing it from the database.
        """
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def approve(self):
        """
        Approves the newsletter and clears any rejection reason.
        """
        self.status = "approved"
        self.approved_at = timezone.now()
        self.rejection_reason = ""
        self.save()

    def reject(self, reason: str):
        """
        Rejects the newsletter with a provided reason.

        Args:
            reason (str): Explanation for the rejection.
        """
        self.status = "rejected"
        self.rejection_reason = reason
        self.save()

    def resubmit(self):
        """
        Resubmits a rejected newsletter for re-review.
        """
        self.status = "submitted"
        self.rejection_reason = ""
        self.save()

    def __str__(self) -> str:
        """
        Returns a string representation of the newsletter.

        Returns:
            str: Title and author's username.
        """
        return f"{self.title} by {self.author.username}"
