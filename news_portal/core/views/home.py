from django.shortcuts import render
from core.models.article import Article
from core.models.newsletter import Newsletter
from core.models.publisher import Publisher
from itertools import chain

def home(request):
    if request.user.is_authenticated:
        user = request.user

        if user.role == "reader":
            publisher_articles = Article.active.filter(
                status="approved", publisher__in=user.subscribed_publishers.all()
            )
            journalist_articles = Article.active.filter(
                status="approved", author__in=user.subscribed_journalists.all()
            )
            newsletters = Newsletter.objects.filter(status="approved", is_deleted=False).order_by("-approved_at")

            combined_articles = list(chain(publisher_articles, journalist_articles))
            sorted_articles = sorted(combined_articles, key=lambda a: a.approved_at or a.created_at, reverse=True)

            return render(
                request,
                "home.html",
                {"articles": sorted_articles, "newsletters": newsletters}
            )

        elif user.role == "journalist":
            articles = Article.objects.filter(author=user, is_deleted=False)
            return render(request, "home.html", {"articles": articles})

        elif user.role == "editor":
            articles = Article.objects.filter(is_deleted=False)
            return render(request, "home.html", {"articles": articles})

        elif user.role == "publisher":
            try:
                publisher = Publisher.objects.get(owner=user)
                articles = Article.objects.filter(publisher=publisher, is_deleted=False)
            except Publisher.DoesNotExist:
                articles = []
            return render(request, "home.html", {"articles": articles})

    # For anonymous users
    articles = Article.active.filter(status="approved").order_by("-approved_at")
    newsletters = Newsletter.objects.filter(status="approved", is_deleted=False).order_by("-approved_at")
    return render(request, "home.html", {"articles": articles, "newsletters": newsletters})
