from django import forms
from core.models.publisher import Publisher
from core.models.user import User


class PublisherForm(forms.ModelForm):
    editors = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(role="editor"), required=False
    )
    journalists = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(role="journalist"), required=False
    )

    class Meta:
        model = Publisher
        fields = ["name", "owner", "editors", "journalists"]
