import os
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from football.models import League


class TestLeagueListCreateView(APITestCase):
    @pytest.mark.django_db
    def setUp(self):
        print(os.environ.get("DATABASE_NAME"))
        url = reverse("league-list-create")
        data = {
            "name": "Liga",
            "country": "Portugal",
            "number_of_teams": 30,
            "current_champion": "Equipa",
            "most_championships": "Equipa",
            "most_appearances": "Jogador"
        }
        self.client.post(url, data, format="json")

    @pytest.mark.django_db
    def test_get(self):
        url = reverse("league-list-create")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

    @pytest.mark.django_db
    def test_post(self):
        url = reverse("league-list-create")
        data = {
            "name": "League",
            "country": "England",
            "number_of_teams": 30,
            "current_champion": "Team",
            "most_championships": "Team",
            "most_appearances": "Player"
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(League.objects.count(), 2)


class TestLeagueRetrieveUpdateDestroy(APITestCase):
    league_id = 0 # setUp() League ID.

    @pytest.mark.django_db
    def setUp(self):
        url = reverse("league-list-create")
        data = {
            "name": "Liga",
            "country": "Portugal",
            "number_of_teams": 30,
            "current_champion": "Equipa",
            "most_championships": "Equipa",
            "most_appearances": "Jogador"
        }
        response = self.client.post(url, data, format="json")
        self.league_id = response.json()["id"]

    @pytest.mark.django_db
    def test_get(self):
        url = reverse("league-retrieve-update-destroy", kwargs={"pk": self.league_id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @pytest.mark.django_db
    def test_put(self):
        url = reverse("league-retrieve-update-destroy", kwargs={"pk": self.league_id})
        data = {
            "name": "Liga",
            "country": "Portugal",
            "number_of_teams": 27,
            "current_champion": "Equipa",
            "most_championships": "Equipa",
            "most_appearances": "Jogador1"
        }
        response = self.client.put(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["number_of_teams"], 27)
        self.assertEqual(response.json()["most_appearances"], "Jogador1")

    @pytest.mark.django_db
    def test_delete(self):
        total_leagues = League.objects.count()

        url = reverse("league-retrieve-update-destroy", kwargs={"pk": self.league_id})
        response = self.client.delete(url)

        self.assertEqual(League.objects.count(), total_leagues - 1)


