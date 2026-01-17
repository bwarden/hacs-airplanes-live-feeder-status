"""Binary sensor platform for airplanes_live_feeder_status."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)

from .entity import AirplanesLiveEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import AirplanesLiveFeederStatusCoordinator
    from .data import AirplanesLiveConfigEntry

ENTITY_DESCRIPTIONS = (
    BinarySensorEntityDescription(
        key="feeder_connected",
        name="Feeder Connected",
        device_class=BinarySensorDeviceClass.CONNECTIVITY,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001
    entry: AirplanesLiveConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the binary_sensor platform."""
    async_add_entities(
        AirplanesLiveBinarySensor(
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class AirplanesLiveBinarySensor(AirplanesLiveEntity, BinarySensorEntity):
    """Airplanes.live binary_sensor class."""

    def __init__(
        self,
        coordinator: AirplanesLiveFeederStatusCoordinator,
        entity_description: BinarySensorEntityDescription,
    ) -> None:
        """Initialize the binary_sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._attr_unique_id = (
            f"{coordinator.config_entry.entry_id}_{entity_description.key}"
        )

    @property
    def is_on(self) -> bool:
        """Return true if the binary_sensor is on."""
        beast_clients = self.coordinator.data.get("beast_clients", [])
        return len(beast_clients) > 0
