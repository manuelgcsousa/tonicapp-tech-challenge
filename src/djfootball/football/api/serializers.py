from rest_framework import serializers

from ..models import League, Team, Player


class LeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = League
        fields = "__all__"


class TeamSerializer(serializers.ModelSerializer):
    league = serializers.StringRelatedField()

    class Meta:
        model = Team 
        fields = "__all__"


class PlayerSerializer(serializers.ModelSerializer):
    # team = TeamSerializer(read_only=True) --> serializes nested objects.
    team = serializers.StringRelatedField()

    class Meta:
        model = Player
        fields = "__all__"

