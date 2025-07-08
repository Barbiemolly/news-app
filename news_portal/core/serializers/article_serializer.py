"""
Serializers for the Article model used in the API layer.

Provides serializers for article retrieval and article creation,
including field-level transformations and validations.
"""

from rest_framework import serializers
from core.models.article import Article


class ArticleSerializer(serializers.ModelSerializer):
    """
    Serializes the Article model for read-only public API views.

    Includes the author's username and the publisher's name as
    additional read-only fields for convenience in frontend display.

    Fields:
        id (int): Unique article ID.
        title (str): Title of the article.
        content (str): Article body content.
        status (str): Editorial status (submitted, approved, rejected).
        author_username (str): The author's username (read-only).
        publisher_name (str): The publisher's name if assigned (read-only).
        created_at (datetime): When the article was created.
        approved_at (datetime): When the article was approved (nullable).
    """

    author_username = serializers.ReadOnlyField(source="author.username")
    publisher_name = serializers.ReadOnlyField(source="publisher.name")

    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "content",
            "status",
            "author_username",
            "publisher_name",
            "created_at",
            "approved_at",
        ]


class ArticleCreateSerializer(serializers.ModelSerializer):
    """
    Handles creation of new articles submitted by journalists.

    This serializer performs validation to ensure the title is unique
    (case-insensitive) and allows optional assignment of a publisher.
    """

    class Meta:
        model = Article
        fields = ["title", "content", "publisher"]

    def validate_title(self, value: str) -> str:
        """
        Validates the uniqueness of the article title (case-insensitive).

        Args:
            value (str): The title provided in the request.

        Raises:
            serializers.ValidationError: If a duplicate title exists.

        Returns:
            str: The validated, unique title.
        """
        if Article.objects.filter(title__iexact=value).exists():
            raise serializers.ValidationError(
                "An article with this title already exists."
            )
        return value
