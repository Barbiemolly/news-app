"""
Unit test for verifying the Article model behavior.
"""

from django.test import TestCase
from core.models.article import Article
from core.models.user import User


class ArticleModelTestCase(TestCase):
    """
    TestCase to verify core behaviors of the Article model.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username="writer", password="testpass", role="journalist"
        )

    def test_article_creation_defaults(self):
        """
        Ensure newly created articles default to 'submitted' status
        and __str__ representation includes title and author.
        """
        article = Article.objects.create(
            title="Test Article", content="Sample content for test.", author=self.user
        )
        self.assertEqual(article.status, "submitted")
        self.assertEqual(str(article), f"Test Article by {self.user.username}")
