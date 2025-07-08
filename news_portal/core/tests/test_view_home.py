"""
Tests for the home view and its article filtering logic.
"""

from django.test import TestCase, Client
from django.urls import reverse
from core.models.user import User
from core.models.article import Article


class HomeViewTestCase(TestCase):
    """
    TestCase for validating article visibility in the home view.
    """

    def setUp(self):
        self.client = Client()
        self.reader = User.objects.create_user(
            username="reader1", password="testpass", role="reader"
        )
        self.journalist = User.objects.create_user(
            username="journalist1", password="testpass", role="journalist"
        )

        self.article1 = Article.objects.create(
            title="Approved Article",
            content="Public content",
            author=self.journalist,
            status="approved",
        )
        self.article2 = Article.objects.create(
            title="Private Article",
            content="Private content",
            author=self.journalist,
            status="submitted",
        )

    def test_reader_sees_only_approved(self):
        """
        Reader should only see approved articles on the homepage.
        """
        self.client.login(username="reader1", password="testpass")
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Approved Article")
        self.assertNotContains(response, "Private Article")
