"""
Moderation views for editors.

Allows editors to review and take action on submitted articles and newsletters.

Functions:
    - moderation_dashboard: Lists all pending items for editor review.
    - approve_newsletter: Marks a newsletter as approved.
    - reject_newsletter: Rejects a newsletter with a reason.
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from core.models.article import Article
from core.models.newsletter import Newsletter


@login_required
def moderation_dashboard(request):
    """
    Displays the moderation dashboard for editors.

    Shows a list of all submitted (pending) articles and newsletters.
    Access:
        - Only users with role 'editor'.

    Template:
        - editor/moderation_dashboard.html

    Context:
        - articles: list of pending Article instances.
        - newsletters: list of pending Newsletter instances.
    """
    if request.user.role != "editor":
        return render(request, "403.html")

    pending_articles = Article.objects.filter(status="submitted", is_deleted=False)
    pending_newsletters = Newsletter.objects.filter(status="submitted", is_deleted=False)

    return render(
        request,
        "editor/moderation_dashboard.html",
        {
            "articles": pending_articles,
            "newsletters": pending_newsletters
        }
    )


@login_required
def approve_newsletter(request, pk):
    """
    Approves a newsletter.

    Sets the status to "approved" and redirects to the moderation dashboard.

    Access:
        - Only users with role 'editor'.

    Args:
        pk (int): Primary key of the newsletter to approve.
    """
    if request.user.role != "editor":
        messages.error(request, "Unauthorized.")
        return redirect("home")

    newsletter = get_object_or_404(Newsletter, pk=pk)
    newsletter.approve()
    messages.success(request, "Newsletter approved.")
    return redirect("moderation_dashboard")


@login_required
def reject_newsletter(request, pk):
    """
    Rejects a newsletter and optionally records a reason.

    Sets the status to "rejected" and stores the rejection reason.

    Access:
        - Only users with role 'editor'.

    Args:
        pk (int): Primary key of the newsletter to reject.
    """
    if request.user.role != "editor":
        messages.error(request, "Unauthorized.")
        return redirect("home")

    newsletter = get_object_or_404(Newsletter, pk=pk)
    reason = request.POST.get("rejection_reason", "No reason provided.")
    newsletter.reject(reason=reason)
    messages.warning(request, "Newsletter rejected.")
    return redirect("moderation_dashboard")
