from django import forms
from core.models.user import User
from core.models.publisher import Publisher


class PublisherEditorForm(forms.ModelForm):
    editors = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(role="editor"),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Publisher
        fields = ["editors"]


class PublisherJournalistForm(forms.ModelForm):
    journalists = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(role="journalist"),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Publisher
        fields = ["journalists"]
