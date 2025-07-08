from django.urls import path
from core.views import article as views
from core.views.moderation import moderation_dashboard, approve_newsletter, reject_newsletter
from core.views.export import export_article_csv, export_article_pdf
from core.views.home import home
from core.views.subscriptions import (
    manage_subscriptions,
    unsubscribe_journalist,
    unsubscribe_publisher,
)
from core.views.profile import publisher_profile, journalist_profile, reader_profile
from core.views.recommendations import article_recommendations
from core.views.bookmark import toggle_bookmark
from core.views import auth as auth_view
from core.views.publisher_dashboard import manage_publisher_roles
from core.views.publisher_dashboard import (
    create_publisher,
    edit_publisher,
    delete_publisher,
)
from core.views import newsletter as newsletter_views

urlpatterns = [
    path("", home, name="home"),
    path("login/", auth_view.user_login, name="login"),
    path("logout/", auth_view.user_logout, name="logout"),
    path("register/", auth_view.user_register, name="register"),
    path("articles/", views.article_list, name="article_list"),
    path("articles/create/", views.create_article, name="create_article"),
    path("articles/<int:pk>/edit/", views.edit_article, name="edit_article"),
    path("articles/<int:pk>/approve/", views.approve_article, name="approve_article"),
    path("articles/<int:pk>/reject/", views.reject_article, name="reject_article"),
    path("articles/<int:pk>/", views.article_detail, name="article_detail"),
    path("moderation/", moderation_dashboard, name="moderation_dashboard"),
    path("export/article/<int:pk>/csv/", export_article_csv, name="export_article_csv"),
    path("export/article/<int:pk>/pdf/", export_article_pdf, name="export_article_pdf"),
    path("subscriptions/", manage_subscriptions, name="manage_subscriptions"),
    path(
        "unsubscribe/publisher/<int:pk>/",
        unsubscribe_publisher,
        name="unsubscribe_publisher",
    ),
    path(
        "unsubscribe/journalist/<int:pk>/",
        unsubscribe_journalist,
        name="unsubscribe_journalist",
    ),
    path("journalist/<int:pk>/", journalist_profile, name="journalist_profile"),
    path("publisher/<int:pk>/", publisher_profile, name="publisher_profile"),
    path("recommendations/", article_recommendations, name="article_recommendations"),
    path("search/", views.search_articles, name="search_articles"),
    path("articles/<int:pk>/bookmark/", toggle_bookmark, name="toggle_bookmark"),
    path("profile/", reader_profile, name="reader_profile"),
    path("trending/", views.trending_articles, name="trending_articles"),
    path(
        "password_reset/",
        auth_view.CustomPasswordResetView.as_view(),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_view.CustomPasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_view.CustomPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_view.CustomPasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path("publisher/manage/", manage_publisher_roles, name="manage_publisher_roles"),
    path("publisher/create/", create_publisher, name="create_publisher"),
    path("publisher/<int:pk>/edit/", edit_publisher, name="edit_publisher"),
    path("publisher/<int:pk>/delete/", delete_publisher, name="delete_publisher"),
    path("article/<int:pk>/delete/", views.delete_article, name="delete_article"),
    path("newsletters/", newsletter_views.newsletter_list, name="newsletter_list"),
    path("newsletters/create/", newsletter_views.create_newsletter, name="create_newsletter"),
    path("newsletters/<int:pk>/", newsletter_views.newsletter_detail, name="newsletter_detail"),
    path("newsletters/<int:pk>/edit/", newsletter_views.edit_newsletter, name="edit_newsletter"),
    path("newsletters/<int:pk>/delete/", newsletter_views.delete_newsletter, name="delete_newsletter"),
    path("newsletter/<int:pk>/approve/", approve_newsletter, name="approve_newsletter"),
    path("newsletter/<int:pk>/reject/", reject_newsletter, name="reject_newsletter"),

]
