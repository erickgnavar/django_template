from django.test import RequestFactory, TestCase
from django.urls import resolve

from .. import views


class HomeViewTestCase(TestCase):
    def setUp(self):
        self.view = views.HomeView.as_view()
        self.factory = RequestFactory()

    def test_match_expected_view(self):
        url = resolve("/")
        self.assertEqual(url.func.__name__, self.view.__name__)

    def test_load_sucessful(self):
        request = self.factory.get("/")
        response = self.view(request)
        self.assertEqual(response.status_code, 200)


class ContactViewTestCase(TestCase):
    def setUp(self):
        self.view = views.contact
        self.factory = RequestFactory()

    def test_match_expected_view(self):
        url = resolve("/contact")
        self.assertEqual(url.func.__name__, self.view.__name__)

    def test_load_sucessful(self):
        request = self.factory.get("/")
        response = self.view(request)
        self.assertEqual(response.status_code, 200)


class PrivacyViewTestCase(TestCase):
    def setUp(self):
        self.view = views.privacy
        self.factory = RequestFactory()

    def test_match_expected_view(self):
        url = resolve("/privacy")
        self.assertEqual(url.func.__name__, self.view.__name__)

    def test_load_sucessful(self):
        request = self.factory.get("/")
        response = self.view(request)
        self.assertEqual(response.status_code, 200)


class CookiesViewTestCase(TestCase):
    def setUp(self):
        self.view = views.cookies
        self.factory = RequestFactory()

    def test_match_expected_view(self):
        url = resolve("/cookies")
        self.assertEqual(url.func.__name__, self.view.__name__)

    def test_load_sucessful(self):
        request = self.factory.get("/")
        response = self.view(request)
        self.assertEqual(response.status_code, 200)


class FaqViewTestCase(TestCase):
    def setUp(self):
        self.view = views.faq
        self.factory = RequestFactory()

    def test_match_expected_view(self):
        url = resolve("/faq")
        self.assertEqual(url.func.__name__, self.view.__name__)

    def test_load_sucessful(self):
        request = self.factory.get("/")
        response = self.view(request)
        self.assertEqual(response.status_code, 200)
