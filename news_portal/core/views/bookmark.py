from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from core.models.article import Article


@login_required
def toggle_bookmark(request, pk):
    article = get_object_or_404(Article, pk=pk, status="approved")
    user = request.user

    if article in user.bookmarked_articles.all():
        user.bookmarked_articles.remove(article)
    else:
        user.bookmarked_articles.add(article)

    return redirect(request.META.get("HTTP_REFERER", "home"))
