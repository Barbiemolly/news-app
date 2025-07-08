from django.db import models
from django.utils import timezone
from core.models.user import User


class Newsletter(models.Model):
    STATUS_CHOICES = [
        ("submitted", "Submitted"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="submitted",
    )
    rejection_reason = models.TextField(blank=True, null=True)

    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="newsletters",
        limit_choices_to={"role": "journalist"},
    )

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def approve(self):
        self.status = "approved"
        self.approved_at = timezone.now()
        self.rejection_reason = ""
        self.save()

    def reject(self, reason):
        self.status = "rejected"
        self.rejection_reason = reason
        self.save()

    def resubmit(self):
        self.status = "submitted"
        self.rejection_reason = ""
        self.save()

    def __str__(self):
        return f"{self.title} by {self.author.username}"
