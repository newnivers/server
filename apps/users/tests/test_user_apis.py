from django.test import TestCase

from apps.users.models import User


class UserModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        User(nickname="test1")
