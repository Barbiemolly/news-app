from core.models.article import Article
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from itertools import chain


@login_required
def article_recommendations(request):
    """
    Recommend articles the reader hasn't seen (not from subscribed publishers or journalists).
    """
    if request.user.role != "reader":
        return redirect("home")

    # Get articles from subscriptions
    by_publisher = Article.active.filter(
        status="approved", publisher__in=request.user.subscribed_publishers.all()
    )
    by_journalist = Article.active.filter(
        status="approved", author__in=request.user.subscribed_journalists.all()
    )

    # Combine seen articles manually
    seen_articles = set(a.id for a in chain(by_publisher, by_journalist))

    # Recommend other unseen approved articles
    recommendations = Article.active.filter(status="approved").exclude(
        id__in=seen_articles
    )[:10]

    return render(
        request, "articles/recommendations.html", {"articles": recommendations}
    )
