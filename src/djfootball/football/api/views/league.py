from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from ...models import League, Player
from ..serializers import LeagueSerializer
from ..paginators import SingleSetPagination


class LeagueListCreateView(APIView):
    """
        get:
        Returns a list of all existing Leagues.
        If query parameter 'player_name' is provided, we return the respective player's League.

        post:
        Creates a new League instance.
    """

    @extend_schema(
        parameters=[
            OpenApiParameter("page", OpenApiTypes.INT, OpenApiParameter.QUERY),
            OpenApiParameter("per_page", OpenApiTypes.INT, OpenApiParameter.QUERY),
            
            OpenApiParameter("player_name", OpenApiTypes.STR, OpenApiParameter.QUERY)
        ],
        description="Returns a list of all existing Leagues. If query parameter 'player_name' is provided, we return the respective player's League.",
        responses=LeagueSerializer
    )
    def get(self, request):
        # default empty response.
        res = JsonResponse({}, safe=False)

        player_name = request.query_params.get("player_name")
        if player_name:
            try:
                # INNER JOIN with 'Team' and 'League' tables.
                player = Player.objects.select_related("team__league").get(name__iexact=player_name)
                
                league = player.team.league
                league_serializer = LeagueSerializer(league)
                
                res = JsonResponse(league_serializer.data, safe=False) 
            except Player.DoesNotExist:
                pass
        else:
            leagues_queryset = League.objects.all().order_by("id")

            if request.query_params.get("page"):
                paginator = SingleSetPagination()

                paginated_queryset = paginator.paginate_queryset(leagues_queryset, request)
                leagues_serializer = LeagueSerializer(paginated_queryset, many=True)

                res = paginator.get_paginated_response(leagues_serializer.data)
            else:
                leagues_serializer = LeagueSerializer(leagues_queryset, many=True)
                
                res = JsonResponse(leagues_serializer.data, safe=False)
        
        return res

    @extend_schema(description="Creates a new League instance.", request=LeagueSerializer, responses=LeagueSerializer)
    def post(self, request):
        # default empty response.
        res = JsonResponse({}, safe=False)
        
        league_serializer = LeagueSerializer(data=request.data)

        if league_serializer.is_valid():
            league_serializer.save()
            res = JsonResponse(league_serializer.data, status=201)
        else:
            res = JsonResponse(league_serializer.errors, status=400)

        return res


class LeagueRetrieveUpdateDestroyView(APIView):
    """
        get:
        Retrieves a given League.

        put:
        Updates a given League.

        patch:
        Partially updates a given League.

        delete:
        Deletes a given League.
    """

    @extend_schema(description="Retrieves a given League.", request=LeagueSerializer, responses=LeagueSerializer)
    def get(self, request, pk):
        league = get_object_or_404(League.objects.all(), pk=pk)
        league_serializer = LeagueSerializer(league)

        return JsonResponse(league_serializer.data, safe=False)

    @extend_schema(description="Updates a given League.", request=LeagueSerializer, responses=LeagueSerializer)
    def put(self, request, pk):
        # default empty response.
        res = JsonResponse({}, safe=False)
        
        stored_league = get_object_or_404(League.objects.all(), pk=pk)
        updated_league = request.data
        
        league_serializer = LeagueSerializer(stored_league, data=updated_league)
        if league_serializer.is_valid():
            league_serializer.save()
            res = JsonResponse(league_serializer.data, status=200)
        else:
            res = JsonResponse(league_serializer.errors, status=400)

        return res

    @extend_schema(description="Partially updates a given League.", request=LeagueSerializer, responses=LeagueSerializer)
    def patch(self, request, pk):
        # default empty response.
        res = JsonResponse({}, safe=False)
        
        stored_league = get_object_or_404(League.objects.all(), pk=pk)
        updated_league = request.data
        
        league_serializer = LeagueSerializer(stored_league, data=updated_league, partial=True)
        if league_serializer.is_valid():
            league_serializer.save()
            res = JsonResponse(league_serializer.data, status=200)
        else:
            res = JsonResponse(league_serializer.errors, status=400)

        return res

    @extend_schema(description="Deletes a given League.", request=LeagueSerializer, responses=LeagueSerializer)
    def delete(self, request, pk):
        league = get_object_or_404(League.objects.all(), pk=pk)
        league.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

