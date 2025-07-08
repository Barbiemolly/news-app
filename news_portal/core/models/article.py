"""
Defines the Article model and its custom manager for the news portal application.

Articles are submitted by journalists and reviewed by editors.
This module includes logic for status transitions, soft deletion, and validation.
"""

from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from core.models.publisher import Publisher
from core.models.user import User


class ActiveArticleManager(models.Manager):
    """
    Custom manager to filter out soft-deleted articles.

    Use `.active.all()` to retrieve only articles where `is_deleted=False`.
    """

    def get_queryset(self):
        """
        Returns a queryset excluding soft-deleted articles.
        """
        return super().get_queryset().filter(is_deleted=False)


class Article(models.Model):
    """
    Represents a news article submitted by a journalist.

    Articles can be approved or rejected by editors. Rejected articles
    can be edited and resubmitted. Soft deletion is supported to allow
    temporary hiding of articles without permanent loss.

    Fields:
        title (str): The article title.
        content (str): The body of the article.
        status (str): Current editorial review status.
        approved_at (datetime): Timestamp of approval.
        is_deleted (bool): Marks article as soft-deleted.
        deleted_at (datetime): Timestamp of soft deletion.
        view_count (int): Number of times the article has been viewed.
        rejection_reason (str): Optional reason provided when rejecting.
        tags (str): Optional tags for searchability.

    Relationships:
        author (User): Journalist who created the article.
        publisher (Publisher): Optional publisher (nullable).
    """

    STATUS_CHOICES = [
        ("submitted", "Submitted"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    title = models.CharField(max_length=255)
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_deleted = models.BooleanField(
        default=False,
        help_text="Soft delete flag. When True, article is hidden but not removed from DB.",
    )
    deleted_at = models.DateTimeField(null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="submitted",
        help_text="Current review status of the article.",
    )

    approved_at = models.DateTimeField(null=True, blank=True)

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="articles",
        limit_choices_to={"role": "journalist"},
        help_text="Author (must have role 'journalist').",
    )

    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="articles",
        help_text="Optional publisher associated with the article.",
    )

    tags = models.CharField(
        max_length=255,
        blank=True,
        help_text="Comma-separated tags for classification and filtering.",
    )

    view_count = models.PositiveIntegerField(default=0)
    rejection_reason = models.TextField(blank=True, null=True)

    objects = models.Manager()  # Default manager
    active = ActiveArticleManager()  # Manager for non-deleted articles

    def clean(self):
        """
        Custom model validation.

        Ensures article titles are unique, ignoring case sensitivity.
        """
        existing = Article.objects.filter(title__iexact=self.title).exclude(pk=self.pk)
        if existing.exists():
            raise ValidationError(
                {"title": "An article with this title already exists."}
            )

    def approve(self):
        """
        Approves the article and sets the approval timestamp.
        """
        self.status = "approved"
        self.approved_at = timezone.now()
        self.save()

    def reject(self):
        """
        Rejects the article and clears any previous approval timestamp.
        """
        self.status = "rejected"
        self.approved_at = None
        self.save()

    def resubmit(self):
        """
        Resubmits a previously rejected article for editor review.

        Only transitions from 'rejected' to 'submitted'.
        """
        if self.status == "rejected":
            self.status = "submitted"
            self.save()

    def soft_delete(self):
        """
        Soft deletes the article without removing it from the database.
        """
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        """
        Restores a previously soft-deleted article.
        """
        self.is_deleted = False
        self.deleted_at = None
        self.save()

    def is_independent(self) -> bool:
        """
        Returns True if the article has no publisher assigned.

        Returns:
            bool: True if the article is independent; False otherwise.
        """
        return self.publisher is None

    def __str__(self) -> str:
        """
        Returns a string representation of the article.

        Returns:
            str: A string in the format "Title by Author".
        """
        return f"{self.title} by {self.author.username}"
