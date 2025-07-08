from django import forms
from core.models.article import Article


class ArticleForm(forms.ModelForm):
    """
    Form for creating and editing articles.
    Title uniqueness is enforced in model clean() method.
    """

    class Meta:
        model = Article
        fields = ["title", "content", "publisher"]
