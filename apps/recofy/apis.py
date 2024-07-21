from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.api.pagination import (
    LimitOffsetPagination,
    get_paginated_response,
)
from apps.recofy.models import Artist
from apps.recofy.serializers import AlbumSerializer, ArtistSerializer, TrackSerializer
from apps.recofy.services.albums import AlbumService
from apps.recofy.services.artists import ArtistService
from apps.recofy.services.tracks import TrackService


class ArtistsListApi(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 1

    def get(self, request: Request):
        all_artists = Artist.objects.prefetch_related("artistimage_set", "genres").all()

        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=ArtistSerializer,
            queryset=all_artists,
            request=request,
            view=self,
        )


class ArtistsRetrieveApi(APIView):
    def get(self, request: Request, artist_id: str):
        artist_service = ArtistService(artist_id=artist_id)
        artist_service.update()
        artist_model = artist_service.retrieve()
        artist = ArtistSerializer(artist_model).data

        return Response(artist)


class AlbumRetrieveApi(APIView):
    def get(self, request: Request, album_id: str):
        market = request.query_params.get("market")
        album_service = AlbumService(album_id=album_id, market=market)
        album_service.update()
        album_model = album_service.retrieve()
        album = AlbumSerializer(album_model).data

        return Response(album)


class TrackRetrieveApi(APIView):
    def get(self, request: Request, track_id: str):
        market = request.query_params.get("market")
        track_service = TrackService(track_id=track_id, market=market)
        track_service.update()
        track_model = track_service.retrieve()
        track = TrackSerializer(track_model).data

        return Response(track)
