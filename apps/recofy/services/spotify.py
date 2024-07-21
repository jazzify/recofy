from abc import ABC, abstractmethod

import requests
from django.core.cache import cache
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.status import HTTP_401_UNAUTHORIZED

from apps.recofy.constants import REDIS_SPOTIFY_ACCESS_TOKEN, SPOTIFY_REQUEST_TIMEOUT
from apps.recofy.utils import spotify_auth


class SpotifyClientService(ABC):
    def _get_headers(self, headers: dict[str, str] | None = None):
        auth_bearer = {
            "Authorization": f"Bearer {cache.get(key=REDIS_SPOTIFY_ACCESS_TOKEN)}"
        }

        if headers:
            return {**auth_bearer, **headers}
        return auth_bearer

    @abstractmethod
    def _prefetch_validation(self) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def _prefetch_url(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def _prefetch_operation(self, data: dict) -> None:
        raise NotImplementedError()

    def update(self):
        self._prefetch_data()

    @spotify_auth
    def get_json_response(self):
        headers = self._get_headers()
        response = requests.get(
            url=self._prefetch_url(), headers=headers, timeout=SPOTIFY_REQUEST_TIMEOUT
        )

        if response.status_code == HTTP_401_UNAUTHORIZED:
            raise AuthenticationFailed("Spotify Base Service")

        return response.json()

    @spotify_auth
    def _prefetch_data(self, headers: dict[str, str] | None = None) -> None:
        if self._prefetch_validation():
            updated_headers = self._get_headers(headers=headers)

            response = requests.get(
                url=self._prefetch_url(),
                headers=updated_headers,
                timeout=SPOTIFY_REQUEST_TIMEOUT,
            )

            if response.status_code == HTTP_401_UNAUTHORIZED:
                raise AuthenticationFailed("Spotify Base Service")

            self._prefetch_operation(
                data=response.json()
            )  # Call child update_or_create_model
