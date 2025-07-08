from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from core.models.article import Article

User = get_user_model()


class ArticleAPITestCase(APITestCase):

    def setUp(self):
        self.journalist = User.objects.create_user(
            username="test_writer", password="testpass123", role="journalist"
        )
        self.token = Token.objects.create(user=self.journalist)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_journalist_can_submit_article(self):
        response = self.client.post(
            "/api/articles/create/",
            {"title": "New API Test", "content": "Sample content", "publisher": ""},
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Article.objects.count(), 1)
        self.assertEqual(Article.objects.first().status, "submitted")

    def test_duplicate_title_fails(self):
        Article.objects.create(
            title="Duplicate",
            content="Test",
            author=self.journalist,
            status="submitted",
        )
        response = self.client.post(
            "/api/articles/create/",
            {"title": "duplicate", "content": "Something new", "publisher": ""},
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("title", response.data)

    def test_article_creation_successful(self):
        response = self.client.post(
            "/api/articles/create/",
            {
                "title": "API Unit Test Article",
                "content": "Test content for article creation.",
            },
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Article.objects.count(), 1)

    def test_article_duplicate_title_case_insensitive(self):
        Article.objects.create(
            title="Unique Title",
            content="Some content",
            author=self.journalist,
            status="submitted",
        )
        response = self.client.post(
            "/api/articles/create/",
            {
                "title": "unique title",  # lowercase duplicate
                "content": "Duplicate check content.",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("title", response.data)

    def test_non_journalist_cannot_create_article(self):
        reader = User.objects.create_user(
            username="reader", password="readerpass", role="reader"
        )
        token = Token.objects.create(user=reader)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        response = self.client.post(
            "/api/articles/create/",
            {"title": "Invalid Submit", "content": "Readers can’t post."},
        )
        self.assertEqual(response.status_code, 400)
