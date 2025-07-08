from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.models.newsletter import Newsletter
from core.forms.newsletter_form import NewsletterForm


@login_required
def newsletter_list(request):
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
    newsletter = get_object_or_404(Newsletter, pk=pk, is_deleted=False)

    if request.user != newsletter.author and request.user.role != "editor":
        messages.error(request, "Unauthorized to delete.")
        return redirect("home")

    newsletter.soft_delete()
    messages.success(request, "Newsletter deleted successfully.")
    return redirect("newsletter_list")


@login_required
def newsletter_detail(request, pk):
    newsletter = get_object_or_404(Newsletter, pk=pk, is_deleted=False)

    if newsletter.status != "approved" and request.user.role not in ["journalist", "editor"]:
        messages.error(request, "Access denied.")
        return redirect("home")

    return render(request, "newsletters/detail.html", {"newsletter": newsletter})
