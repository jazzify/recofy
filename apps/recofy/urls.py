from django.urls import path

from apps.recofy import apis

urlpatterns = [
    path("artists/", apis.ArtistsListApi.as_view(), name="artist_list"),
    path(
        "artists/<str:artist_id>/",
        apis.ArtistsRetrieveApi.as_view(),
        name="artist_retrieve",
    ),
    path(
        "albums/<str:album_id>/", apis.AlbumRetrieveApi.as_view(), name="album_retrieve"
    ),
    path(
        "tracks/<str:track_id>/", apis.TrackRetrieveApi.as_view(), name="track_retrieve"
    ),
]
