import unittest

from django.contrib.auth import get_user_model
from django.test import TestCase

from . import TestHelper


User = get_user_model()


class TestHelperTest(TestCase):
    def test_create_user(self):
        user = TestHelper.create_user(username='tester')
        self.assertTrue(User.objects.filter(id=user.id).exists())
        self.assertEqual(user.credential['username'], 'tester')
        self.assertTrue(user.credential['password'])
