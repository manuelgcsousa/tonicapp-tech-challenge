import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from football.models import Team


class TestTeamListCreateView(APITestCase):
    @pytest.mark.django_db
    def setUp(self):
        url = reverse("team-list-create")
        data = {
            "name": "Equipa",
            "city": "Porto",
            "championships_won": 27,
            "coach": "Treinador",
            "number_of_players": 27
        }
        self.client.post(url, data, format="json")

    @pytest.mark.django_db
    def test_get(self):
        url = reverse("team-list-create")
        response = self.client.get(url)
 
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

    @pytest.mark.django_db
    def test_post(self):
        url = reverse("team-list-create")
        data = {
            "name": "Team",
            "city": "Lisbon",
            "championships_won": 1,
            "coach": "Coach",
            "number_of_players": 1
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Team.objects.count(), 2)


class TestTeamRetrieveUpdateDestroy(APITestCase):
    team_id = 0 # setUp() Team ID.

    @pytest.mark.django_db
    def setUp(self):
        url = reverse("team-list-create")
        data = {
            "name": "Equipa",
            "city": "Porto",
            "championships_won": 27,
            "coach": "Treinador",
            "number_of_players": 27
        }
        response = self.client.post(url, data, format="json")
        self.team_id = response.json()["id"]

    @pytest.mark.django_db
    def test_get(self):
        url = reverse("team-retrieve-update-destroy", kwargs={"pk": self.team_id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @pytest.mark.django_db
    def test_put(self):
        url = reverse("team-retrieve-update-destroy", kwargs={"pk": self.team_id})
        data = {
            "name": "Equipa",
            "city": "Porto",
            "championships_won": 1,
            "coach": "Treinador",
            "number_of_players": 1
        }
        response = self.client.put(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["championships_won"], 1)
        self.assertEqual(response.json()["number_of_players"], 1)

    @pytest.mark.django_db
    def test_delete(self):
        total_teams = Team.objects.count()

        url = reverse("team-retrieve-update-destroy", kwargs={"pk": self.team_id})
        response = self.client.delete(url)

        self.assertEqual(Team.objects.count(), total_teams - 1)


