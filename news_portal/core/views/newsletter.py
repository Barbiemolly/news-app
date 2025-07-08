"""
Views for managing newsletters in the news portal system.

Allows journalists to create, update, and view their newsletters,
while editors can moderate all. Readers can view approved newsletters only.

Functions:
    - newsletter_list: Lists newsletters based on user role.
    - create_newsletter: Allows a journalist to create a newsletter.
    - edit_newsletter: Allows journalist or editor to update a newsletter.
    - delete_newsletter: Soft-deletes a newsletter.
    - newsletter_detail: Displays newsletter content with access control.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.models.newsletter import Newsletter
from core.forms.newsletter_form import NewsletterForm


@login_required
def newsletter_list(request):
    """
    Lists newsletters based on the user's role:

    - Journalist: sees their own newsletters.
    - Editor: sees all newsletters.
    - Reader: sees only approved newsletters.

    Template:
        - newsletters/list.html

    Context:
        - newsletters (QuerySet): Filtered newsletters for display.
    """
    user = request.user

    if user.role == "journalist":
        newsletters = Newsletter.objects.filter(author=user, is_deleted=False)
    elif user.role == "editor":
        newsletters = Newsletter.objects.filter(is_deleted=False)
    elif user.role == "reader":
        newsletters = Newsletter.objects.filter(status="approved", is_deleted=False)
    else:
        return redirect("home")

    return render(request, "newsletters/list.html", {"newsletters": newsletters})


@login_required
def create_newsletter(request):
    """
    Allows a journalist to create and submit a newsletter.

    Access:
        - Only users with role 'journalist'.

    Template:
        - newsletters/form.html
    """
    if request.user.role != "journalist":
        return redirect("home")

    form = NewsletterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        newsletter = form.save(commit=False)
        newsletter.author = request.user
        newsletter.save()
        messages.success(request, "Newsletter created successfully.")
        return redirect("newsletter_list")

    return render(request, "newsletters/form.html", {"form": form})


@login_required
def edit_newsletter(request, pk):
    """
    Allows a journalist or editor to edit an existing newsletter.

    Access:
        - Journalist (only own newsletter)
        - Editor (any newsletter)

    Template:
        - newsletters/form.html

    Args:
        pk (int): Primary key of the newsletter to edit.
    """
    newsletter = get_object_or_404(Newsletter, pk=pk, is_deleted=False)

    if request.user != newsletter.author and request.user.role != "editor":
        return redirect("home")

    form = NewsletterForm(request.POST or None, instance=newsletter)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Newsletter updated successfully.")
        return redirect("newsletter_list")

    return render(request, "newsletters/form.html", {"form": form})


@login_required
def delete_newsletter(request, pk):
    """
    Soft-deletes a newsletter (hides from display but keeps in DB).

    Access:
        - Only the newsletter's author or an editor.

    Redirects:
        - Back to the newsletter list after action.

    Args:
        pk (int): Primary key of the newsletter to delete.
    """
    newsletter = get_object_or_404(Newsletter, pk=pk, is_deleted=False)

    if request.user != newsletter.author and request.user.role != "editor":
        messages.error(request, "Unauthorized to delete.")
        return redirect("home")

    newsletter.soft_delete()
    messages.success(request, "Newsletter deleted successfully.")
    return redirect("newsletter_list")


@login_required
def newsletter_detail(request, pk):
    """
    Displays full content of a newsletter.

    Access:
        - Readers: only approved newsletters.
        - Journalists: own newsletters.
        - Editors: all newsletters.

    Template:
        - newsletters/detail.html

    Args:
        pk (int): Primary key of the newsletter to display.
    """
    newsletter = get_object_or_404(Newsletter, pk=pk, is_deleted=False)

    if newsletter.status != "approved" and request.user.role not in ["journalist", "editor"]:
        messages.error(request, "Access denied.")
        return redirect("home")

    return render(request, "newsletters/detail.html", {"newsletter": newsletter})
