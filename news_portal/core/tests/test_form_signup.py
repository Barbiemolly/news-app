"""
Tests for the SignUp form to ensure user registration is validated properly.
"""

from django.test import TestCase
from core.forms.register_form import SignUpForm


class SignUpFormTestCase(TestCase):
    """
    TestCase for verifying validation behavior of the SignUp form.
    """

    def test_valid_signup_form(self):
        """
        Should pass with valid data and a secure password.
        """
        form = SignUpForm(
            data={
                "username": "testuser",
                "email": "test@example.com",
                "role": "reader",
                "password1": "ComplexPass123!",
                "password2": "ComplexPass123!",
            }
        )
        self.assertTrue(form.is_valid())

    def test_password_mismatch(self):
        """
        Should fail if passwords do not match.
        """
        form = SignUpForm(
            data={
                "username": "user2",
                "email": "user2@example.com",
                "role": "reader",
                "password1": "Password123!",
                "password2": "WrongPass123!",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

    def test_common_password_rejection(self):
        """
        Should reject weak or common passwords.
        """
        form = SignUpForm(
            data={
                "username": "user3",
                "email": "user3@example.com",
                "role": "reader",
                "password1": "password",
                "password2": "password",
            }
        )
        self.assertFalse(form.is_valid())
