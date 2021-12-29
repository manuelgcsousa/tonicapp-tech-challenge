import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from football.models import Player


class TestPlayerListCreateView(APITestCase):
    @pytest.mark.django_db
    def setUp(self):
        url = reverse("player-list-create")
        data = {
            "team": "Equipa",
            "name": "Jogador",
            "age": 27,
            "position": "Atacante",
            "appearances": 200
        }
        self.client.post(url, data, format="json")

    @pytest.mark.django_db
    def test_get(self):
        url = reverse("player-list-create")
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

    @pytest.mark.django_db
    def test_post(self):
        url = reverse("player-list-create")
        data = {
            "team": "Team",
            "name": "Player",
            "age": 27,
            "position": "Forward",
            "appearances": 200
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Player.objects.count(), 2)


class TestPlayerRetrieveUpdateDestroy(APITestCase):
    player_id = 0 # setUp() Team ID.

    @pytest.mark.django_db
    def setUp(self):
        url = reverse("player-list-create")
        data = {
            "team": "Equipa",
            "name": "Jogador",
            "age": 27,
            "position": "Atacante",
            "appearances": 200
        }
        response = self.client.post(url, data, format="json")
        self.player_id = response.json()["id"]

    @pytest.mark.django_db
    def test_get(self):
        url = reverse("player-retrieve-update-destroy", kwargs={"pk": self.player_id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @pytest.mark.django_db
    def test_put(self):
        url = reverse("player-retrieve-update-destroy", kwargs={"pk": self.player_id})
        data = {
            "team": "Equipa",
            "name": "Jogador",
            "age": 27,
            "position": "Defender",
            "appearances": 201
        }
        response = self.client.put(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["position"], "Defender")
        self.assertEqual(response.json()["appearances"], 201)

    @pytest.mark.django_db
    def test_delete(self):
        total_players = Player.objects.count()

        url = reverse("player-retrieve-update-destroy", kwargs={"pk": self.player_id})
        response = self.client.delete(url)

        self.assertEqual(Player.objects.count(), total_players - 1)


