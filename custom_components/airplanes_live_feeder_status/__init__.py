"""
Custom integration to integrate airplanes.live feeder status with Home Assistant.

For more details about this integration, please refer to
https://github.com/bwarden/hacs-airplanes-live-feeder-status
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.const import Platform
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import AirplanesLiveApiClient
from .coordinator import AirplanesLiveFeederStatusCoordinator
from .data import AirplanesLiveFeederStatusData

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from .data import AirplanesLiveConfigEntry

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: AirplanesLiveConfigEntry,
) -> bool:
    """Set up this integration using UI."""
    coordinator = AirplanesLiveFeederStatusCoordinator(
        hass=hass,
        client=AirplanesLiveApiClient(
            session=async_get_clientsession(hass),
        ),
    )
    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = AirplanesLiveFeederStatusData(coordinator=coordinator)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: AirplanesLiveConfigEntry,
) -> bool:
    """Handle removal of an entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
