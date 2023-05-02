from django.test import TestCase
from base.forms import RoomForm
from base.models import Room, Topic, User

class RoomFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='johndoe',
            email='johndoe@example.com',
            password='password'
        )
        self.topic = Topic.objects.create(name='Test Topic')
        self.host = User.objects.create(username='testuser', email='testuser@example.com', password='testpassword')
        self.topic = Topic.objects.create(name='Test Topic')
        
    def test_room_form_valid(self):
        data = {
            'host': self.user.id,
            'topic': self.topic.id,
            'name': 'Test Room',
            'description': 'Test Description',
            'participants': [self.user.id]
        }
        form = RoomForm(data=data)
        self.assertTrue(form.is_valid())
        
    def test_room_form_invalid(self):
        data = {
            'host': self.user.id,
            'topic': self.topic.id,
            'name': '',
            'description': 'Test Description',
            'participants': [self.user.id]
        }
        form = RoomForm(data=data)
        self.assertFalse(form.is_valid())

    def test_room_form_valid_data(self):
        user = User.objects.create(email='test@example.com', password='password')
        topic = Topic.objects.create(name='test topic')
        data = {
            'host': user.id,
            'topic': topic.id,
            'name': 'test room',
            'description': 'test description',
        }
        form = RoomForm(data=data)
        self.assertTrue(form.is_valid())

    def test_room_form_blank_data(self):
        form = RoomForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)

    def test_room_form_valid_data(self):
        form = RoomForm({
            'topic': self.topic.pk,
            'name': 'Test Room',
            'description': 'This is a test room',
        })
        self.assertTrue(form.is_valid())
        room = form.save()
        self.assertEqual(room.topic, self.topic)
        self.assertEqual(room.name, 'Test Room')
        self.assertEqual(room.description, 'This is a test room')
    