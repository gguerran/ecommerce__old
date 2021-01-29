from datetime import datetime

from django.test import TestCase

from ecommerce.accounts.models import User


class UserModelTest(TestCase):
    def setUp(self):
        self.user = User(username='test')
        self.user.set_password('#pass123')
        self.user.save()

    def test_create(self):
        self.assertTrue(User.objects.exists())

    def test_str(self):
        self.assertEquals(str(self.user), 'test')

    def test_username(self):
        self.assertEquals(self.user.username, 'test')

    def test_created(self):
        self.assertIsInstance(self.user.created, datetime)

    def test_modified(self):
        self.assertIsInstance(self.user.modified, datetime)

    def test_name_can_not_be_blank_and_null(self):
        field = User._meta.get_field('username')
        self.assertFalse(field.blank)
        self.assertFalse(field.null)

    def test_check_pass(self):
        password = '#pass123'
        self.assertTrue(self.user.check_password(password))

    def test_check_pass_wrong(self):
        password = '#pass1234'
        self.assertFalse(self.user.check_password(password))

    def test_default_is_active(self):
        self.assertTrue(self.user.is_active)

    def test_default_is_superuser(self):
        self.assertFalse(self.user.is_superuser)
