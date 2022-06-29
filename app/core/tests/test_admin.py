"""
Tests for the Django admin modifications
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client

class AdminSiteTests(TestCase):
    """Tests for Django admin"""

    def setUp(self):
        """Create User and Client"""
        self.client = Client()  #use client for creating http request
         #creating superuser
        self.admin_user=get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='testpass123',
        )
        #creating new user
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            password='test123',
            name='test user',
        )

    def test_users_list(self):
        """Test that users are listed on page"""
        url = reverse('admin:core_user_changelist') #getting url of user list
        res = self.client.get(url) #making http request of the url

        self.assertContains(res,self.user.name) #testing whether name is correct or not
        self.assertContains(res,self.user.email) ##testing whether email is correct or not

    def test_edit_user_page(self):
        """Test the edit user page works."""
        url = reverse('admin:core_user_change', args=[self.user.id]) #url for edit user page
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test the create user page works."""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)