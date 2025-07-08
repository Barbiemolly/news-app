from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from core.models.article import Article

User = get_user_model()


class ArticleApprovalTests(APITestCase):

    def setUp(self):
        # Create users
        self.editor = User.objects.create_user(
            username="editor_user", password="editorpass", role="editor"
        )
        self.journalist = User.objects.create_user(
            username="journalist_user", password="journalistpass", role="journalist"
        )
        self.token_editor = Token.objects.create(user=self.editor)
        self.token_journalist = Token.objects.create(user=self.journalist)

        # Create article
        self.article = Article.objects.create(
            title="Editor Approval Test",
            content="Editor approval test content.",
            author=self.journalist,
            status="submitted",
        )

    def test_editor_can_approve_article(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Token " + self.token_editor.key)

        response = client.post(f"/api/articles/{self.article.id}/approve/")
        self.assertEqual(response.status_code, 200)
        self.article.refresh_from_db()
        self.assertEqual(self.article.status, "approved")

    def test_editor_can_reject_article(self):
        # Reset article status
        self.article.status = "submitted"
        self.article.save()

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Token " + self.token_editor.key)

        response = client.post(f"/api/articles/{self.article.id}/reject/")
        self.assertEqual(response.status_code, 200)
        self.article.refresh_from_db()
        self.assertEqual(self.article.status, "rejected")

    def test_journalist_cannot_approve_article(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Token " + self.token_journalist.key)

        response = client.post(f"/api/articles/{self.article.id}/approve/")
        self.assertEqual(response.status_code, 403)
        self.article.refresh_from_db()
        self.assertEqual(self.article.status, "submitted")

    def test_cannot_reapprove_approved_article(self):
        self.article.status = "approved"
        self.article.save()

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Token " + self.token_editor.key)

        response = client.post(f"/api/articles/{self.article.id}/approve/")
        self.assertEqual(response.status_code, 404)
