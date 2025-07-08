from rest_framework import generics, permissions, serializers, status, filters
from rest_framework.permissions import IsAuthenticated
from core.models.article import Article
from core.serializers.article_serializer import (
    ArticleSerializer,
    ArticleCreateSerializer,
)
from rest_framework.views import APIView
from rest_framework.response import Response


class PublicArticleListView(generics.ListAPIView):
    """
    Public API: View all approved articles.
    """

    queryset = Article.objects.filter(status="approved")
    serializer_class = ArticleSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "content", "author__username"]
    ordering_fields = ["created_at", "approved_at"]


class PublisherArticleListView(generics.ListAPIView):
    """
    View articles by publisher ID (approved only).
    """

    serializer_class = ArticleSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Article.objects.filter(
            publisher__id=self.kwargs["publisher_id"], status="approved"
        )


class JournalistArticleListView(generics.ListAPIView):
    """
    View articles by journalist ID (approved only).
    """

    serializer_class = ArticleSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Article.objects.filter(
            author__id=self.kwargs["journalist_id"], status="approved"
        )


class ArticleCreateView(generics.CreateAPIView):
    """
    Allows journalists to create/submit an article via API.
    """

    serializer_class = ArticleCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        if user.role != "journalist":
            raise serializers.ValidationError("Only journalists may submit articles.")
        serializer.save(author=user, status="submitted")


class ApproveArticleView(APIView):
    """
    API endpoint for editors to approve an article.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        user = request.user
        if user.role != "editor":
            return Response({"detail": "Permission denied."}, status=403)

        try:
            article = Article.objects.get(pk=pk, status="submitted")
        except Article.DoesNotExist:
            return Response(
                {"detail": "Article not found or already processed."}, status=404
            )

        article.approve()
        return Response({"detail": "Article approved successfully."}, status=200)


class RejectArticleView(APIView):
    """
    API endpoint for editors to reject an article.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        user = request.user
        if user.role != "editor":
            return Response({"detail": "Permission denied."}, status=403)

        try:
            article = Article.objects.get(pk=pk, status="submitted")
        except Article.DoesNotExist:
            return Response(
                {"detail": "Article not found or already processed."}, status=404
            )

        article.reject()
        return Response({"detail": "Article rejected successfully."}, status=200)
