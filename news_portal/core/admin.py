from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.utils.timezone import localtime
from django.utils.translation import gettext_lazy as _
from core.models.user import User
from core.models.publisher import Publisher
from core.models.article import Article

# -------------------------------
# Custom User Admin
# -------------------------------


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Admin configuration for the custom User model.
    Adds role field to user creation and editing forms.
    """

    fieldsets = BaseUserAdmin.fieldsets + (
        (_("Role Information"), {"fields": ("role",)}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (_("Role Information"), {"fields": ("role",)}),
    )

    list_display = ("username", "email", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")
    search_fields = ("username", "email")
    ordering = ("username",)

    filter_horizontal = ("subscribed_journalists", "subscribed_publishers")


# -------------------------------
# Publisher Admin
# -------------------------------


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    """
    Admin configuration for Publisher model.
    """

    list_display = ("name", "description")
    search_fields = ("name",)
    filter_horizontal = ("editors", "journalists")


# -------------------------------
# Article Admin
# -------------------------------


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """
    Admin configuration for Article model.
    Displays workflow status, timestamps, and reviewer controls.
    """

    list_display = (
        "title",
        "author",
        "publisher",
        "status_colored",
        "approved_at_local",
        "created_at",
        "updated_at",
    )
    list_filter = ("status", "publisher", "created_at")
    search_fields = ("title", "content", "author__username")
    readonly_fields = ("created_at", "updated_at", "approved_at")
    actions = ["soft_delete_selected", "restore_selected"]

    def status_colored(self, obj):
        """
        Shows status with basic coloring for visual feedback.
        """
        color = {"submitted": "orange", "approved": "green", "rejected": "red"}.get(
            obj.status, "black"
        )
        return format_html(
            '<b style="color: {};">{}</b>', color, obj.status.capitalize()
        )

    status_colored.short_description = "Status"

    def approved_at_local(self, obj):
        """
        Displays approved_at in readable format.
        """
        return (
            localtime(obj.approved_at).strftime("%Y-%m-%d %H:%M")
            if obj.approved_at
            else "-"
        )

    approved_at_local.short_description = "Approved At"

    def soft_delete_selected(self, request, queryset):
        for article in queryset:
            article.soft_delete()
        self.message_user(request, "Selected articles were soft-deleted.")

    soft_delete_selected.short_description = "Soft delete selected articles"

    def restore_selected(self, request, queryset):
        for article in queryset:
            article.restore()
        self.message_user(request, "Selected articles were restored.")

    restore_selected.short_description = "Restore selected articles"
