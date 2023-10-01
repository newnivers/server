from unittest import TestCase

from django.db import IntegrityError

from apps.users.models import User


class UserModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def test_create_user_model_success(self):
        with self.assertRaises(IntegrityError):
            User.objects.create(nickname="test")
        self.assertEqual(len(User.objects.all()), 1)

    def test_create_user_model_failed_duplicate_nickname(self):
        with self.assertRaises(IntegrityError):
            User.objects.create(nickname="test")
        self.assertEqual(len(User.objects.all()), 1)
