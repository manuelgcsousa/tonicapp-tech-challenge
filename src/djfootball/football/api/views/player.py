from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from ...models import Player
from ..serializers import PlayerSerializer
from ..paginators import SingleSetPagination


class PlayerListCreateView(APIView):
    """
        get:
        Returns a list of all existing Players.

        post:
        Creates a new Player instance.
    """

    @extend_schema(
        parameters=[
            OpenApiParameter("page", OpenApiTypes.INT, OpenApiParameter.QUERY),
            OpenApiParameter("per_page", OpenApiTypes.INT, OpenApiParameter.QUERY),
        ],
        description="Returns a list of all existing Players.",
        responses=PlayerSerializer
    )
    def get(self, request):
        # default empty response.
        res = JsonResponse({}, safe=False)

        players_queryset = Player.objects.all().order_by("id")
        if request.query_params.get("page"):
            paginator = SingleSetPagination()

            paginated_queryset = paginator.paginate_queryset(players_queryset, request)
            players_serializer = PlayerSerializer(paginated_queryset, many=True)

            res = paginator.get_paginated_response(players_serializer.data)
        else:
            players_serializer = PlayerSerializer(players_queryset, many=True)

            res = JsonResponse(players_serializer.data, safe=False)
        
        return res

    @extend_schema(description="Creates a new Player instance.", request=PlayerSerializer, responses=PlayerSerializer)
    def post(self, request):
        # default empty response.
        res = JsonResponse({}, safe=False)
        
        player_serializer = PlayerSerializer(data=request.data)

        if player_serializer.is_valid():
            player_serializer.save()
            res = JsonResponse(player_serializer.data, status=201)
        else:
            res = JsonResponse(player_serializer.errors, status=400)

        return res


class PlayerRetrieveUpdateDestroyView(APIView):
    """
        get:
        Retrieves a given Player.

        put:
        Updates a given Player.

        patch:
        Partially updates a given Player.

        delete:
        Deletes a given Player.
    """

    @extend_schema(description="Retrieves a given Player.", request=PlayerSerializer, responses=PlayerSerializer)
    def get(self, request, pk):
        player = get_object_or_404(Player.objects.all(), pk=pk)
        player_serializer = PlayerSerializer(player)

        return JsonResponse(player_serializer.data, safe=False)

    @extend_schema(description="Updates a given Player.", request=PlayerSerializer, responses=PlayerSerializer)
    def put(self, request, pk):
        # default empty response.
        res = JsonResponse({}, safe=False)
        
        stored_player = get_object_or_404(Player.objects.all(), pk=pk)
        updated_player = request.data
        
        player_serializer = PlayerSerializer(stored_player, data=updated_player)
        if player_serializer.is_valid():
            player_serializer.save()
            res = JsonResponse(player_serializer.data, status=200)
        else:
            res = JsonResponse(player_serializer.errors, status=400)

        return res

    @extend_schema(description="Partially updates a given Player.", request=PlayerSerializer, responses=PlayerSerializer)
    def patch(self, request, pk):
        # default empty response.
        res = JsonResponse({}, safe=False)
        
        stored_player = get_object_or_404(Player.objects.all(), pk=pk)
        updated_player = request.data
        
        player_serializer = PlayerSerializer(stored_player, data=updated_player, partial=True)
        if player_serializer.is_valid():
            player_serializer.save()
            res = JsonResponse(player_serializer.data, status=200)
        else:
            res = JsonResponse(player_serializer.errors, status=400)

        return res

    @extend_schema(description="Deletes a given Player.", request=PlayerSerializer, responses=PlayerSerializer)
    def delete(self, request, pk):
        player = get_object_or_404(Player.objects.all(), pk=pk)
        player.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

