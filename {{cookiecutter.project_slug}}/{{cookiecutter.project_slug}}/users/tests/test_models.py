from django.test import TestCase

from ..models import User


class UserTestCase(TestCase):
    def test_str(self):
        user = User(email="demo")
        self.assertEqual(str(user), "demo")
