from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from core.models.publisher import Publisher
from core.models.user import User


@login_required
def manage_subscriptions(request):
    if request.user.role != "reader":
        return redirect("home")

    publishers = Publisher.objects.all()
    journalists = User.objects.filter(role="journalist")

    if request.method == "POST":
        selected_publishers = request.POST.getlist("publishers")
        selected_journalists = request.POST.getlist("journalists")

        request.user.subscribed_publishers.set(selected_publishers)
        request.user.subscribed_journalists.set(selected_journalists)
        request.user.save()

        return redirect("home")

    return render(
        request,
        "subscriptions/manage.html",
        {
            "publishers": publishers,
            "journalists": journalists,
            "selected_publishers": request.user.subscribed_publishers.all(),
            "selected_journalists": request.user.subscribed_journalists.all(),
        },
    )


@login_required
def unsubscribe_publisher(request, pk):
    if request.user.role != "reader":
        return redirect("home")
    request.user.subscribed_publishers.remove(pk)
    return redirect("manage_subscriptions")


@login_required
def unsubscribe_journalist(request, pk):
    if request.user.role != "reader":
        return redirect("home")
    request.user.subscribed_journalists.remove(pk)
    return redirect("manage_subscriptions")
