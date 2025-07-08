from rest_framework import serializers
from core.models.article import Article


class ArticleSerializer(serializers.ModelSerializer):
    """
    Serializes Article model for public API view.
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
    Handles article creation from journalists.
    """

    class Meta:
        model = Article
        fields = ["title", "content", "publisher"]

    def validate_title(self, value):
        """
        Prevents duplicate titles, case-insensitive.
        """
        if Article.objects.filter(title__iexact=value).exists():
            raise serializers.ValidationError(
                "An article with this title already exists."
            )
        return value
