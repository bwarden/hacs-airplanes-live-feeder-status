"""Airplanes.live Feeder Status API Client."""

from __future__ import annotations

import socket
from typing import Any

import aiohttp
import async_timeout

from .const import URL_FEED_STATUS


class AirplanesLiveApiClientError(Exception):
    """Exception to indicate a general API error."""


class AirplanesLiveApiClientCommunicationError(
    AirplanesLiveApiClientError,
):
    """Exception to indicate a communication error."""


class AirplanesLiveApiClient:
    """Airplanes.live API Client."""

    def __init__(
        self,
        session: aiohttp.ClientSession,
    ) -> None:
        """Initialize the API Client."""
        self._session = session

    async def async_get_data(self) -> Any:
        """Get data from the API."""
        return await self._api_wrapper(
            method="get",
            url=URL_FEED_STATUS,
        )

    async def _api_wrapper(
        self,
        method: str,
        url: str,
        data: dict | None = None,
        headers: dict | None = None,
    ) -> Any:
        """Get information from the API."""
        try:
            async with async_timeout.timeout(10):
                response = await self._session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=data,
                )
                response.raise_for_status()
                return await response.json()

        except TimeoutError as exception:
            msg = f"Timeout error fetching information - {exception}"
            raise AirplanesLiveApiClientCommunicationError(
                msg,
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            msg = f"Error fetching information - {exception}"
            raise AirplanesLiveApiClientCommunicationError(
                msg,
            ) from exception
        except Exception as exception:  # pylint: disable=broad-except
            msg = f"Something really wrong happened! - {exception}"
            raise AirplanesLiveApiClientError(
                msg,
            ) from exception
