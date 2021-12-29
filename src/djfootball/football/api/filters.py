import django_filters

from ..models import Team


class TeamFilter(django_filters.FilterSet):
    name  = django_filters.CharFilter(lookup_expr="iexact")
    city  = django_filters.CharFilter(lookup_expr="iexact")
    coach = django_filters.CharFilter(lookup_expr="iexact")

    class Meta:
        model = Team
        fields = ("name", "city", "championships_won", "coach", "number_of_players")
