from django.urls import path
from core.api import views as api_views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path("articles/", api_views.PublicArticleListView.as_view(), name="api_articles"),
    path(
        "publisher/<int:publisher_id>/articles/",
        api_views.PublisherArticleListView.as_view(),
        name="api_publisher_articles",
    ),
    path(
        "journalist/<int:journalist_id>/articles/",
        api_views.JournalistArticleListView.as_view(),
        name="api_journalist_articles",
    ),
    path("token/", obtain_auth_token, name="api_token_auth"),
    path(
        "articles/create/",
        api_views.ArticleCreateView.as_view(),
        name="api_article_create",
    ),
    path(
        "articles/<int:pk>/approve/",
        api_views.ApproveArticleView.as_view(),
        name="api_article_approve",
    ),
    path(
        "articles/<int:pk>/reject/",
        api_views.RejectArticleView.as_view(),
        name="api_article_reject",
    ),
]
