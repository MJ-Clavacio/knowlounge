from django.test import TestCase
from base.forms import MyUserCreationForm, RoomForm, UserForm
from base.models import User, Room

class TestForms(TestCase):

    def test_myusercreationform_valid_data(self):
        form = MyUserCreationForm(data={
            'name': 'Test User',
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123',
        })

        self.assertTrue(form.is_valid())

    def test_myusercreationform_invalid_data(self):
        form = MyUserCreationForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 5)

    def test_userform_valid_data(self):
        user = User.objects.create_user(username='testuser', password='testpass123')
        form = UserForm(data={
            'name': 'Test User',
            'username': 'testuser',
            'email': 'testuser@example.com',
            'bio': 'Test Bio',
        }, instance=user)

        self.assertTrue(form.is_valid())

    def test_userform_invalid_data(self):
        form = UserForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 4)


