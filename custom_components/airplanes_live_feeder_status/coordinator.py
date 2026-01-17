"""DataUpdateCoordinator for airplanes_live_feeder_status."""

from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING, Any

from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .api import AirplanesLiveApiClientError
from .const import DOMAIN, LOGGER

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from .api import AirplanesLiveApiClient
    from .data import AirplanesLiveConfigEntry


# https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
class AirplanesLiveFeederStatusCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    config_entry: AirplanesLiveConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        client: AirplanesLiveApiClient,
    ) -> None:
        """Initialize."""
        self.client = client
        super().__init__(
            hass=hass,
            logger=LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=1),
        )

    async def _async_update_data(self) -> Any:
        """Update data via library."""
        try:
            return await self.client.async_get_data()
        except AirplanesLiveApiClientError as exception:
            raise UpdateFailed(exception) from exception
