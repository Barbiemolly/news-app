from django.shortcuts import render, get_object_or_404, redirect
from core.models.user import User
from core.models.publisher import Publisher
from django.contrib.auth.decorators import login_required


def journalist_profile(request, pk):
    journalist = get_object_or_404(User, pk=pk, role="journalist")
    subscriber_count = journalist.followers.count()
    return render(
        request,
        "profiles/journalist_profile.html",
        {
            "journalist": journalist,
            "subscriber_count": subscriber_count,
        },
    )


def publisher_profile(request, pk):
    publisher = get_object_or_404(Publisher, pk=pk)
    subscriber_count = publisher.subscribers.count()
    return render(
        request,
        "profiles/publisher_profile.html",
        {
            "publisher": publisher,
            "subscriber_count": subscriber_count,
        },
    )


@login_required
def reader_profile(request):
    if request.user.role != "reader":
        return redirect("home")

    bookmarks = request.user.bookmarked_articles.all()
    subs_pubs = request.user.subscribed_publishers.all()
    subs_journos = request.user.subscribed_journalists.all()

    return render(
        request,
        "profiles/reader_profile.html",
        {"bookmarks": bookmarks, "subs_pubs": subs_pubs, "subs_journos": subs_journos},
    )
