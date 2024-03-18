# tests.py
import json

from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse

from .utils import generate_access_token
from .views import SearchAPIView
from .tasks import log_search


class SearchAPIViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')

    def test_search_api_view_unauthenticated(self):
        url = reverse('app:search')  # Update the reverse call
        request = self.factory.get(url, {'hostname': 'example.com'})

        response = SearchAPIView.as_view()(request)
        self.assertEqual(response.status_code, 401)
        # You can further assert the response content if needed

    # Add more test cases for other scenarios as needed


class LogSearchTaskTestCase(TestCase):
    def test_log_search_task(self):
        # Create a mock kwargs for the task
        kwargs = {'username': 'testuser', 'key': 'hostname', 'value': 'example.com'}

        # Call the task
        result = log_search.apply(kwargs=kwargs)

        # Assert that the task has executed successfully
        self.assertTrue(result.successful())
        # You can further assert other conditions related to the task result
