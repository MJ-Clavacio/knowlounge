from django.test import TestCase, Client
from django.urls import reverse
from base.models import Room, Topic, Message, User

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.home_url = reverse('home')
        self.register_url = reverse('register')
        self.user1 = User.objects.create_user(username='testuser1', password='testpass123')
        self.topic1 = Topic.objects.create(name='test topic 1')
        self.room1 = Room.objects.create(host=self.user1, topic=self.topic1, name='test room 1', description='test description')
        self.message1 = Message.objects.create(user=self.user1, room=self.room1, body='test message 1')

    def test_login_page_GET(self):
        response = self.client.get(self.login_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/login_register.html')
        self.assertContains(response, 'Login')

    def test_register_page_GET(self):
        response = self.client.get(self.register_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/login_register.html')
        self.assertContains(response, 'Register')

    def test_home_page_GET(self):
        response = self.client.get(self.home_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/home.html')
        self.assertContains(response, 'room')

    def test_room_page_GET(self):
        response = self.client.get(reverse('room', args=[self.room1.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/room.html')
        self.assertContains(response, 'test room 1')

    def test_create_room_POST(self):
        response = self.client.post(reverse('create-room'), {'name': 'test room 2'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Room.objects.count(), 1)
        self.assertEqual(Room.objects.last().name, 'test room 1')

    def test_update_room_POST(self):
        room = Room.objects.create(name='test room 1')
        response = self.client.post(reverse('update-room', args=[room.pk]), {'name': 'test room 3'})
        self.assertEqual(response.status_code, 302)
        room.refresh_from_db()
        self.assertEqual(room.name, 'test room 1')

    def test_delete_room_POST(self):
        room = Room.objects.create(name='test room 1')
        response = self.client.post(reverse('delete-room', args=[room.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Room.objects.count(), 2)

    def test_room_page_GET_with_existing_messages(self):
        message1 = Message.objects.create(user=self.user1, room=self.room1, body='test message 1')
        message2 = Message.objects.create(user=self.user1, room=self.room1, body='test message 2')
        message3 = Message.objects.create(user=self.user1, room=self.room1, body='test message 3')
        
        response = self.client.get(reverse('room', args=[self.room1.id]))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/room.html')
        self.assertContains(response, 'test room 1')
        self.assertContains(response, 'test message 1')
        self.assertContains(response, 'test message 2')
        self.assertContains(response, 'test message 3')

    def test_delete_message_POST(self):
        self.client.login(username='testuser1', password='testpass123')
        message = Message.objects.create(user=self.user1, room=self.room1, body='test message 2')
        response = self.client.post(reverse('delete-message', args=[message.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Message.objects.count(), 2)