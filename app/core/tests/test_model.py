"""
Test for Models
"""

from django.test import TestCase
from django.contrib.auth import get_user_model #to retrieve model



class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful"""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email = email,
            password = password,
        )

        self.assertEqual(user.email,email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self): #to normalize email
        """Test email is normalized for new users"""
        sample_emails=[
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]

        for email,expected in sample_emails: #to variables in for loop because two items in sample_emails array
            user=get_user_model().objects.create_user(email,'sample123')
            self.assertEqual(user.email,expected)

    def test_new_user_without_email_raises_error(self):
        """test that creating user without an email raises a value error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('','test123')

    def test_create_super_user(self):
        """Test creating a superuser"""
        user=get_user_model().objects.create_superuser(
            'test@example.com',
            'test123',
        )

        self.assertTrue(user.is_superuser) #provided by permissions mixin
        self.assertTrue(user.is_staff)
