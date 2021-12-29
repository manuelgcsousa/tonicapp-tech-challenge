from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from ...models import Team
from ..filters import TeamFilter
from ..serializers import TeamSerializer
from ..paginators import SingleSetPagination


class TeamListCreateView(APIView):
    """
        get:
        Returns a list of all existing Teams.
        Possibility to filter teams: ('name', 'city', 'championships_won', 'coach', 'number_of_players')

        post:
        Creates a new Team instance.
    """

    @extend_schema(
        parameters=[
            OpenApiParameter("page", OpenApiTypes.INT, OpenApiParameter.QUERY),
            OpenApiParameter("per_page", OpenApiTypes.INT, OpenApiParameter.QUERY),
            
            OpenApiParameter("name", OpenApiTypes.STR, OpenApiParameter.QUERY),
            OpenApiParameter("city", OpenApiTypes.STR, OpenApiParameter.QUERY),
            OpenApiParameter("championships_won", OpenApiTypes.INT, OpenApiParameter.QUERY),
            OpenApiParameter("coach", OpenApiTypes.STR, OpenApiParameter.QUERY),
            OpenApiParameter("number_of_players", OpenApiTypes.INT, OpenApiParameter.QUERY)
        ],
        description="Returns a list of all existing Teams.",
        responses=TeamSerializer
    )
    def get(self, request):
        # default empty response.
        res = JsonResponse({}, safe=False)

        teams_queryset = Team.objects.all().order_by("id")
        
        filterset = TeamFilter(request.GET, queryset=teams_queryset)
        if filterset.is_valid():
            teams_queryset = filterset.qs
            
        if request.query_params.get("page"):
            paginator = SingleSetPagination()

            paginated_queryset = paginator.paginate_queryset(teams_queryset, request)
            teams_serializer = TeamSerializer(paginated_queryset, many=True)

            res = paginator.get_paginated_response(teams_serializer.data)
        else:
            teams_serializer = TeamSerializer(teams_queryset, many=True)
            
            res = JsonResponse(teams_serializer.data, safe=False)
        
        return res

    @extend_schema(description="Creates a new Team instance.", request=TeamSerializer, responses=TeamSerializer)
    def post(self, request):
        # default empty response.
        res = JsonResponse({}, safe=False)
        
        team_serializer = TeamSerializer(data=request.data)

        if team_serializer.is_valid():
            team_serializer.save()
            res = JsonResponse(team_serializer.data, status=201)
        else:
            res = JsonResponse(team_serializer.errors, status=400)

        return res


class TeamRetrieveUpdateDestroyView(APIView):
    """
        get:
        Retrieves a given Team.

        put:
        Updates a given Team.

        patch:
        Partially updates a given Team.

        delete:
        Deletes a given Team.
    """

    @extend_schema(description="Retrieves a given Team.", request=TeamSerializer, responses=TeamSerializer)
    def get(self, request, pk):
        team = get_object_or_404(Team.objects.all(), pk=pk)
        team_serializer = TeamSerializer(team)

        return JsonResponse(team_serializer.data, safe=False)

    @extend_schema(description="Updates a given Team.", request=TeamSerializer, responses=TeamSerializer)
    def put(self, request, pk):
        # default empty response.
        res = JsonResponse({}, safe=False)
        
        stored_team = get_object_or_404(Team.objects.all(), pk=pk)
        updated_team = request.data
        
        team_serializer = TeamSerializer(stored_team, data=updated_team)
        if team_serializer.is_valid():
            team_serializer.save()
            res = JsonResponse(team_serializer.data, status=200)
        else:
            res = JsonResponse(team_serializer.errors, status=400)

        return res

    @extend_schema(description="Partially updates a given Team.", request=TeamSerializer, responses=TeamSerializer)
    def patch(self, request, pk):
        # default empty response.
        res = JsonResponse({}, safe=False)
        
        stored_team = get_object_or_404(Team.objects.all(), pk=pk)
        updated_team = request.data
        
        team_serializer = TeamSerializer(stored_team, data=updated_team, partial=True)
        if team_serializer.is_valid():
            team_serializer.save()
            res = JsonResponse(team_serializer.data, status=200)
        else:
            res = JsonResponse(team_serializer.errors, status=400)

        return res

    @extend_schema(description="Deletes a given Team.", request=TeamSerializer, responses=TeamSerializer)
    def delete(self, request, pk):
        team = get_object_or_404(Team.objects.all(), pk=pk)
        team.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

