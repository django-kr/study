# coding: utf-8
'''
TODO:

v signup : just make user model with deactivated status
v verification(email) : make user activate
_ unregistration
_ change user informations
_ authentication
'''
import json
import datetime

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.core import mail
from django.utils.timezone import now
from django.conf import settings

from ..models import SignupVerification
from . import TestHelper

User = get_user_model()


class SignupProcessTest(TestCase, TestHelper):
    def setUp(self):
        self.test_credential = {
            'username': 'test_user',
            'email': 'test_user@testemail.com',
            'password': 'testpassword',
        }

    def test_signup(self):
        """new user should be inactive"""
        resp = self.client.post(self.signup_url, self.test_credential)
        self.assertEqual(resp.status_code, 200)
        registed_user = User.objects.filter(username=self.test_credential['username'],
                                            is_active=False)
        self.assertTrue(registed_user)

    def test_signup_verification(self):
        """email should be sent"""
        resp = self.client.post(self.signup_url, self.test_credential)

        self.assertEqual(len(mail.outbox), 1)
        email_message = str(mail.outbox[0].message())
        # Verification model instance should be created.
        sv = SignupVerification.objects.get(user__username=self.test_credential['username'])
        self.assertTrue(sv.key)
        self.assertIn(sv.key, email_message)

    def test_verification(self):
        resp = self.client.post(self.signup_url, self.test_credential)
        sv = SignupVerification.objects.get(user__username=self.test_credential['username'])
        resp = self.client.get(reverse('activation', kwargs={'key': sv.key}))
        self.assertEqual(resp.status_code, 200)
        user = User.objects.get(username=self.test_credential['username'])
        self.assertTrue(user.is_active)

    def test_verfication_fail_on_expired_key(self):
        resp = self.client.post(self.signup_url, self.test_credential)
        sv = SignupVerification.objects.get(user__username=self.test_credential['username'])
        sv.created_at = now() - settings.ACTIVATION_EXPIRE - datetime.timedelta(days=1)
        sv.save()
        resp = self.client.get(reverse('activation', kwargs={'key': sv.key}))
        self.assertEqual(resp.status_code, 400)
        user = User.objects.get(username=self.test_credential['username'])
        self.assertFalse(user.is_active)
