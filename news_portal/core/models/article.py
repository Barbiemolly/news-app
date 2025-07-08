from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from core.models.publisher import Publisher
from core.models.user import User


class ActiveArticleManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class Article(models.Model):
    """
    Represents a news article submitted by a journalist.
    Editors can approve or reject submitted articles.
    Rejected articles can be edited and resubmitted.
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

    is_deleted = models.BooleanField(default=False, help_text="Soft delete flag")
    deleted_at = models.DateTimeField(null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="submitted",
        help_text="Current review status of the article",
    )

    approved_at = models.DateTimeField(null=True, blank=True)

    # Relationships
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="articles",
        limit_choices_to={"role": "journalist"},
        help_text="Author (must be a journalist)",
    )

    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="articles",
        help_text="Optional publisher",
    )

    objects = models.Manager()  # Default
    active = ActiveArticleManager()  # Use .active.all() to only get undeleted
    tags = models.CharField(max_length=255, blank=True)
    view_count = models.PositiveIntegerField(default=0)
    rejection_reason = models.TextField(blank=True, null=True)

    def clean(self):
        """
        Custom validation: prevent duplicate article titles (case-insensitive).
        """
        existing = Article.objects.filter(title__iexact=self.title).exclude(pk=self.pk)
        if existing.exists():
            raise ValidationError(
                {"title": "An article with this title already exists."}
            )

    def approve(self):
        """
        Approves the article and sets the timestamp.
        """
        self.status = "approved"
        self.approved_at = timezone.now()
        self.save()

    def reject(self):
        """
        Rejects the article.
        """
        self.status = "rejected"
        self.approved_at = None
        self.save()

    def resubmit(self):
        """
        Resubmits a previously rejected article for review.
        """
        if self.status == "rejected":
            self.status = "submitted"
            self.save()

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        self.is_deleted = False
        self.deleted_at = None
        self.save()

    def is_independent(self):
        return self.publisher is None

    def __str__(self):
        return f"{self.title} by {self.author.username}"
