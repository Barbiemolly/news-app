"""
Views for managing article-related operations in the news portal.

Includes article creation, editing, approval, rejection, searching,
listing, detail views, trending articles, and soft deletion.

All views enforce role-based access control.

Functions:
    - create_article: Journalist submits a new article.
    - edit_article: Journalist edits and resubmits a rejected article.
    - approve_article: Editor approves a submitted article.
    - reject_article: Editor rejects a submitted article with reason.
    - article_list: Lists articles based on user role.
    - article_detail: Displays article content with access control.
    - search_articles: Search for articles by title, content, or tags.
    - trending_articles: Displays top 5 most viewed articles.
    - delete_article: Soft-deletes an article (editor or author).
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from collections import Counter
from core.models.article import Article
from core.forms.article_form import ArticleForm
from core.forms.reject_form import RejectForm


@login_required
def create_article(request):
    """
    Allows a journalist to create and submit a new article.

    Access:
        - Only users with role 'journalist'.

    Template:
        - articles/create.html
    """
    if request.user.role != "journalist":
        messages.error(request, "You do not have permission to create articles.")
        return redirect("home")

    form = ArticleForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        article.status = "submitted"
        article.save()
        messages.success(request, "Article submitted for review.")
        return redirect("article_list")

    return render(request, "articles/create.html", {"form": form})


@login_required
def edit_article(request, pk):
    """
    Allows journalists to edit and resubmit a rejected article.

    Access:
        - Only authors of the rejected article.

    Template:
        - articles/edit.html
    """
    article = get_object_or_404(Article, pk=pk, author=request.user)

    if article.status != "rejected":
        messages.warning(request, "Only rejected articles can be edited.")
        return redirect("article_list")

    form = ArticleForm(request.POST or None, instance=article)

    if request.method == "POST" and form.is_valid():
        article = form.save(commit=False)
        article.resubmit()
        article.save()
        messages.success(request, "Article resubmitted.")
        return redirect("article_list")

    return render(request, "articles/edit.html", {"form": form})


@login_required
def approve_article(request, pk):
    """
    Allows editors to approve a submitted article.

    Access:
        - Only users with role 'editor'.
    """
    if request.user.role != "editor":
        messages.error(request, "Permission denied.")
        return redirect("home")

    article = get_object_or_404(Article, pk=pk, status="submitted")
    article.approve()
    article.save()
    messages.success(request, "Article approved.")
    return redirect("article_list")


@login_required
def reject_article(request, pk):
    """
    Allows editors to reject a submitted article with a reason.

    Access:
        - Only users with role 'editor'.

    Template:
        - editor/reject.html
    """
    if request.user.role != "editor":
        messages.error(request, "Permission denied.")
        return redirect("home")

    article = get_object_or_404(Article, pk=pk, status="submitted")

    if request.method == "POST":
        form = RejectForm(request.POST)
        if form.is_valid():
            article.rejection_reason = form.cleaned_data["reason"]
            article.status = "rejected"
            article.save()
            messages.warning(request, "Article rejected with reason.")
            return redirect("article_list")
    else:
        form = RejectForm()

    return render(request, "editor/reject.html", {"form": form, "article": article})


@login_required
def article_list(request):
    """
    Lists articles based on user's role:

    - Reader: sees approved articles.
    - Journalist: sees their own articles.
    - Editor: sees all articles.

    Template:
        - articles/list.html
    """
    user = request.user
    if user.role == "reader":
        articles = Article.objects.filter(status="approved", is_deleted=False)
    elif user.role == "journalist":
        articles = Article.objects.filter(author=user, is_deleted=False)
    elif user.role == "editor":
        articles = Article.objects.filter(is_deleted=False)
    else:
        articles = Article.objects.none()

    paginator = Paginator(articles.order_by("-created_at"), 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "articles/list.html", {"articles": page_obj})


@login_required
def article_detail(request, pk):
    """
    Displays the full content of an article with access restrictions.

    Access Rules:
        - Reader: only approved articles.
        - Journalist: only own articles.
        - Editor: all articles.

    Template:
        - articles/detail.html
    """
    article = get_object_or_404(Article, pk=pk)

    if request.user.role == "reader" and article.status != "approved":
        messages.warning(request, "You do not have access to this article.")
        return redirect("article_list")

    if request.user.role == "journalist" and article.author != request.user:
        messages.warning(request, "Access denied.")
        return redirect("article_list")

    article.view_count += 1
    article.save()

    return render(request, "articles/detail.html", {"article": article})


def search_articles(request):
    """
    Allows users to search for articles using title, content, or tags.

    Also displays the top 5 most-used tags for suggestions.

    Template:
        - articles/search_results.html
    """
    query = request.GET.get("q")
    results = Article.active.filter(status="approved")

    if query:
        results = results.filter(
            Q(title__icontains=query)
            | Q(content__icontains=query)
            | Q(tags__icontains=query)
        )

    paginator = Paginator(results.order_by("-approved_at"), 10)
    page_number = request.GET.get("page")
    results = paginator.get_page(page_number)

    all_tags = Article.objects.values_list("tags", flat=True)
    tags_flat = [tag.strip() for tags in all_tags if tags for tag in tags.split(",")]
    top_tags = Counter(tags_flat).most_common(5)

    return render(
        request,
        "articles/search_results.html",
        {"query": query, "results": results, "top_tags": top_tags},
    )


def trending_articles(request):
    """
    Displays the top 5 most-viewed articles.

    Template:
        - articles/trending.html
    """
    articles = Article.active.filter(status="approved").order_by("-view_count")[:5]
    return render(request, "articles/trending.html", {"articles": articles})


@login_required
def delete_article(request, pk):
    """
    Soft deletes an article.

    Access:
        - Author of the article.
        - Publisher's owner.
        - Publisher's assigned editor.

    Redirects:
        - Redirects to home after deletion or failure.
    """
    article = get_object_or_404(Article, pk=pk)
    if (
        request.user == article.author
        or request.user in article.publisher.editors.all()
        or request.user == article.publisher.owner
    ):
        article.is_deleted = True
        article.save()
        messages.success(request, "Article deleted successfully.")
    else:
        messages.error(request, "You are not authorized to delete this article.")
    return redirect("home")
