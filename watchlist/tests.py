from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from watchlist import models

class StreamPlatformList(APITestCase):
     def setUp(self): # creating setup data user and stream
            self.user=User.objects.create_user(username="haa",password="haa@123")
            self.token=Token.objects.get(user__username="haa")
            self.client.credentials(HTTP_AUTHORIZATION='Token '+self.token.key)
            self.stream= models.StreamPlatform.objects.create(name="Netflix",
            about="#1 Streaming",
            website="https://net.com")
     def test_streamplatform_create(self):
        data={
            "name":"Netflix",
            "about":"#1 Streaming",
            "website":"https://net.com"
        }
        response=self.client.post(reverse('streams-detail'),data)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)# since stream can be created by only admin so normal user will get this status code
     def test_streamplatfrom_id(self):
         response=self.client.get(reverse('streamplatform-detail',args=(self.stream.id,)))#passing id as args to reverse method
         self.assertEqual(response.status_code,status.HTTP_200_OK)

class WatchlistPla(APITestCase):
    def setUp(self):
        self.user=User.objects.create_user(username="haa",password="haa@123")
        self.token=Token.objects.get(user__username="haa")
        self.client.credentials(HTTP_AUTHORIZATION='Token '+self.token.key)
        self.stream= models.StreamPlatform.objects.create(name="Netflix",
            about="#1 Streaming",
            website="https://net.com")
        self.watchlist=models.WatchList.objects.create(platform=self.stream,title="cghghgxhx",
        storyline="xBSDJHVF",active=True)
    def test_watch(self):
            data={
            "platform":self.stream,
            "title":"cghghgxhx",
            "storyline":"xBSDJHVF",
            "active":True
            }
            response=self.client.post(reverse('movie-details'),data)
            self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
        
    def test_watchlist(self):
          response=self.client.get(reverse('movie-details'))
          self.assertEqual(response.status_code,status.HTTP_200_OK)
    def test_watchlist_ind(self):
          response=self.client.get(reverse('movie',args=(self.watchlist.id,)))
          self.assertEqual(response.status_code,status.HTTP_200_OK)
     