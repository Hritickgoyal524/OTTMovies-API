from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from watchlist import models

class RegTestCase(APITestCase):
    def test_register(self):
        data={
            "username":"Exmaple",
            "email":"testcase@gmail.com",
            "password":"newpass@123",
            "password2":"newpass@123"
        }
        response=self.client.post(reverse('registration'),data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
# Create your tests here.

class Loginlogout(APITestCase):
    def setUp(self):
        self.user=User.objects.create_user(username="haa",password="haa@123")
    def test_login(self):
        data={
            "username":"haa",
            "password":"haa@123"

        }
        response=self.client.post(reverse('login'),data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    def test_logout(self):
        self.token=Token.objects.get(user__username="haa")
        self.client.credentials(HTTP_AUTHORIZATION='Token '+self.token.key)
        response=self.client.post(reverse('logout'))
        self.assertEqual(response.status_code,status.HTTP_200_OK)

