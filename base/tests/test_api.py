from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from base.models import Room

class TestAPIViews(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_getRoutes(self):
        url = reverse('getRoutes')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, ["GET /api", "GET /api/rooms", "GET /api/rooms/:id"])

    def test_getRooms(self):
        Room.objects.create(name='room1', description='description1')
        Room.objects.create(name='room2', description='description2')

        url = reverse('getRooms')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_getRoom(self):
        room = Room.objects.create(name='room1', description='description1')

        url = reverse('getRoom', args=[room.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'room1')
        self.assertEqual(response.data['description'], 'description1')
