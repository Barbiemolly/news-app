"""
Views for managing publishers, including creation, editing, deletion,
and assigning editors and journalists to publishing houses.

Access is restricted based on user roles, primarily the publisher (owner).

Functions:
    - manage_publisher_roles: Assigns editors and journalists to a publisher.
    - create_publisher: Creates a new publisher with assigned roles.
    - edit_publisher: Allows the publisher owner to update their profile.
    - delete_publisher: Soft-deletes a publisher entity (owner only).
"""

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from core.models.publisher import Publisher
from core.forms.publisher_management_form import PublisherEditorForm, PublisherJournalistForm
from core.forms.publisher_creation_form import PublisherForm
from core.models.user import User
from core.models.article import Article


@login_required
def manage_publisher_roles(request):
    """
    Allows a publisher to assign editors and journalists to their publishing house.

    Access:
        - Only the logged-in user who owns the publisher profile.

    Template:
        - publisher/manage_roles.html

    Context:
        - Forms for assigning editors and journalists.
        - Lists of paired and unpaired users.
    """
    try:
        publisher = Publisher.objects.get(owner=request.user)
    except Publisher.DoesNotExist:
        messages.warning(request, "You don't have a publisher yet.")
        return redirect("create_publisher")

    if request.method == "POST":
        editor_form = PublisherEditorForm(request.POST, instance=publisher)
        journalist_form = PublisherJournalistForm(request.POST, instance=publisher)

        if editor_form.is_valid() and journalist_form.is_valid():
            publisher.editors.set(editor_form.cleaned_data["editors"])
            publisher.journalists.set(journalist_form.cleaned_data["journalists"])
            publisher.save()
            messages.success(request, "Editors and journalists successfully paired.")
            return redirect("manage_publisher_roles")
    else:
        editor_form = PublisherEditorForm(instance=publisher)
        journalist_form = PublisherJournalistForm(instance=publisher)

    all_editors = User.objects.filter(role="editor")
    all_journalists = User.objects.filter(role="journalist")

    paired_editors = publisher.editors.all()
    paired_journalists = publisher.journalists.all()

    unpaired_editors = all_editors.exclude(id__in=paired_editors)
    unpaired_journalists = all_journalists.exclude(id__in=paired_journalists)

    return render(
        request,
        "publisher/manage_roles.html",
        {
            "editor_form": editor_form,
            "journalist_form": journalist_form,
            "paired_editors": paired_editors,
            "paired_journalists": paired_journalists,
            "unpaired_editors": unpaired_editors,
            "unpaired_journalists": unpaired_journalists,
        },
    )


@login_required
def create_publisher(request):
    """
    Creates a new publisher profile and assigns initial editors and journalists.

    Access:
        - Logged-in users.

    Template:
        - publisher/create_manage.html

    Context:
        - PublisherForm for creation.
        - All publishers for reference/admin view.
    """
    if request.method == "POST":
        form = PublisherForm(request.POST)
        if form.is_valid():
            publisher = form.save(commit=False)
            publisher.save()
            form.save_m2m()
            messages.success(request, "Publisher created and roles assigned successfully.")
            return redirect("home")
    else:
        form = PublisherForm()

    all_publishers = Publisher.objects.select_related("owner").prefetch_related("editors", "journalists")

    return render(
        request,
        "publisher/create_manage.html",
        {
            "form": form,
            "publishers": all_publishers,
        },
    )


@login_required
def edit_publisher(request, pk):
    """
    Allows a publisher owner to update their publishing house information.

    Access:
        - Only the owner of the publisher.

    Template:
        - publisher/edit_publisher.html

    Args:
        pk (int): Primary key of the publisher to edit.

    Context:
        - PublisherForm
        - Articles linked to the publisher
    """
    publisher = get_object_or_404(Publisher, pk=pk)

    if publisher.owner != request.user:
        messages.warning(request, "You are not authorized to edit this publisher. Can only edit a publishing house under your name!")
        return redirect("home")

    if request.method == "POST":
        form = PublisherForm(request.POST, instance=publisher)
        if form.is_valid():
            form.save()
            messages.success(request, "Publisher updated successfully.")
            return redirect("home")
    else:
        form = PublisherForm(instance=publisher)

    publisher_articles = Article.objects.filter(publisher=publisher, is_deleted=False)

    return render(
        request,
        "publisher/edit_publisher.html",
        {
            "form": form,
            "publisher": publisher,
            "articles": publisher_articles,
        },
    )


@login_required
def delete_publisher(request, pk):
    """
    Soft-deletes a publisher.

    Access:
        - Only the owner of the publisher.

    Redirects:
        - To home after deletion or access denial.

    Args:
        pk (int): Primary key of the publisher to delete.
    """
    publisher = get_object_or_404(Publisher, pk=pk)

    if request.user == publisher.owner:
        publisher.is_deleted = True
        publisher.save()
        messages.success(request, "Publisher deleted successfully.")
    else:
        messages.error(request, "You are not authorized to delete this publisher.")

    return redirect("home")
