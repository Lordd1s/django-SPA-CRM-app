from django.contrib.auth.models import User
from django.test import TestCase


from final_course.models import UserProfile
from unittest.mock import patch
from rest_framework.test import APIRequestFactory
from final_course.views import (
    news_to_front,
)

# Create your tests here.



from django.test import TestCase, Client
from unittest.mock import patch
from final_course.utils import CustomCache


class NewsToFrontTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    @patch("final_course.utils.CustomCache.get_cache")
    def test_news_to_front_cached(self, mock_get_cache):
        mock_get_cache.return_value = {
            "title": "Mocked News",
            "content": "This is a mocked news",
        }

        response = self.client.get("/newsletter/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "title": "Mocked News",
                "content": "This is a mocked news",
            },
        )

    @patch("final_course.utils.CustomCache.get_cache")
    @patch("final_course.utils.news")
    def test_news_to_front_not_cached(self, mock_news, mock_get_cache):
        mock_get_cache.return_value = None
        mock_news.return_value = {
            "articles": [{"title": "New News", "content": "This is a new news"}]
        }

        response = self.client.get("/newsletter/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"articles": [{"title": "New News", "content": "This is a new news"}]},
        )

    @patch("final_course.utils.CustomCache.get_cache")
    @patch("final_course.utils.news")
    def test_news_to_front_exception(self, mock_news, mock_get_cache):
        mock_get_cache.return_value = None
        mock_news.side_effect = Exception("Some error occurred")

        response = self.client.get("/newsletter/")

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {"message": "Some error occurred"})
