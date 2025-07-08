from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from core.forms.register_form import SignUpForm
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            role = getattr(user, "role", None)
            if role == "reader":
                return redirect("home")
            elif role == "journalist":
                return redirect("article_list")
            elif role == "editor":
                return redirect("moderation_dashboard")
            elif role == "publisher":
                return redirect("home")
            else:
                return redirect("home")  # Fallback
        else:
            messages.error(request, "Invalid username or password.")

    # Always return the login page on GET (or after failed POST)
    return render(request, "auth/login.html")


def user_logout(request):
    logout(request)
    return redirect("login")


def user_register(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Account created successfully. Please log in.")
            return redirect("login")
    else:
        form = SignUpForm()
    return render(request, "auth/register.html", {"form": form})


class CustomPasswordResetView(SuccessMessageMixin, auth_views.PasswordResetView):
    template_name = "auth/password_reset.html"  # Form to enter email
    email_template_name = "auth/password_reset_email.html"  # Email body
    subject_template_name = "auth/password_reset_subject.txt"  # Email subject
    success_url = reverse_lazy("password_reset_done")
    success_message = "We've emailed you instructions for setting your password."


class CustomPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = "auth/password_reset_done.html"  # Message that email was sent


class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = "auth/password_reset_confirm.html"  # Form to set new password
    success_url = reverse_lazy("password_reset_complete")


class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = "auth/password_reset_complete.html"  # Success message after reset
