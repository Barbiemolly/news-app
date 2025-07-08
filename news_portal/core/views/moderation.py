from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from core.models.article import Article
from core.models.newsletter import Newsletter


@login_required
def moderation_dashboard(request):
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
    if request.user.role != "editor":
        messages.error(request, "Unauthorized.")
        return redirect("home")

    newsletter = get_object_or_404(Newsletter, pk=pk)
    newsletter.approve()
    messages.success(request, "Newsletter approved.")
    return redirect("moderation_dashboard")


@login_required
def reject_newsletter(request, pk):
    if request.user.role != "editor":
        messages.error(request, "Unauthorized.")
        return redirect("home")

    newsletter = get_object_or_404(Newsletter, pk=pk)
    reason = request.POST.get("rejection_reason", "No reason provided.")
    newsletter.reject(reason=reason)
    messages.warning(request, "Newsletter rejected.")
    return redirect("moderation_dashboard")
