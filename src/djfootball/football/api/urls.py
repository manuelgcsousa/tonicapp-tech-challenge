from django.urls import path

from .views import league, team, player


urlpatterns = [
    # leagues
    path("leagues/", league.LeagueListCreateView.as_view(), name="league-list-create"),
    path("leagues/<int:pk>", league.LeagueRetrieveUpdateDestroyView.as_view(), name="league-retrieve-update-destroy"),
    
    # teams
    path("teams/", team.TeamListCreateView.as_view(), name="team-list-create"),
    path("teams/<int:pk>", team.TeamRetrieveUpdateDestroyView.as_view(), name="team-retrieve-update-destroy"),

    # players
    path("players/", player.PlayerListCreateView.as_view(), name="player-list-create"),
    path("players/<int:pk>", player.PlayerRetrieveUpdateDestroyView.as_view(), name="player-retrieve-update-destroy"),
]
