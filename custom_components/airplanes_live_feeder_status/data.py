"""Custom types for airplanes_live_feeder_status."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from homeassistant.config_entries import ConfigEntry

if TYPE_CHECKING:
    from .coordinator import AirplanesLiveFeederStatusCoordinator


type AirplanesLiveConfigEntry = ConfigEntry[AirplanesLiveFeederStatusData]


@dataclass
class AirplanesLiveFeederStatusData:
    """Data for the Airplanes.live Feeder Status integration."""

    coordinator: AirplanesLiveFeederStatusCoordinator