"""Sensor platform for airplanes_live_feeder_status."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription

from .entity import AirplanesLiveEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import AirplanesLiveFeederStatusCoordinator
    from .data import AirplanesLiveConfigEntry

ENTITY_DESCRIPTIONS = (
    SensorEntityDescription(
        key="host",
        name="Feeder Host",
        icon="mdi:ip-network",
    ),
    SensorEntityDescription(
        key="map_link",
        name="Map Link",
        icon="mdi:map",
    ),
    SensorEntityDescription(
        key="msgs_s",
        name="Messages per Second",
        icon="mdi:message-processing",
        native_unit_of_measurement="msg/s",
    ),
    SensorEntityDescription(
        key="pos_s",
        name="Positions per Second",
        icon="mdi:crosshairs-gps",
        native_unit_of_measurement="pos/s",
    ),
    SensorEntityDescription(
        key="avg_kbit_s",
        name="Bandwidth",
        icon="mdi:network",
        native_unit_of_measurement="kbit/s",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: AirplanesLiveConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    async_add_entities(
        AirplanesLiveSensor(
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class AirplanesLiveSensor(AirplanesLiveEntity, SensorEntity):
    """Airplanes.live Sensor class."""

    def __init__(
        self,
        coordinator: AirplanesLiveFeederStatusCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._attr_unique_id = (
            f"{coordinator.config_entry.entry_id}_{entity_description.key}"
        )

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""
        data = self.coordinator.data
        key = self.entity_description.key

        if key in ["host", "map_link"]:
            return data.get(key)

        # For client stats, we take the first beast client if available
        beast_clients = data.get("beast_clients", [])
        if beast_clients:
            client = beast_clients[0]
            return client.get(key)

        # Default to 0 for stats if no client connected
        if key in ["msgs_s", "pos_s", "avg_kbit_s"]:
            return 0

        return None
