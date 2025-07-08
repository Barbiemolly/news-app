from django import forms


class RejectForm(forms.Form):
    reason = forms.CharField(
        label="Rejection Reason",
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        required=True,
    )
