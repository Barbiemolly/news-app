from django import forms
from django.contrib.auth.forms import UserCreationForm
from core.models.user import User
from core.models.publisher import Publisher


class SignUpForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.ROLE_CHOICES)

    class Meta:
        model = User
        fields = ["username", "email", "role", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)

        if commit:
            user.save()
            # Auto-create Publisher if selected
            if user.role == "publisher":
                Publisher.objects.create(
                    name=f"{user.username}'s Publisher", owner=user
                )

        return user
