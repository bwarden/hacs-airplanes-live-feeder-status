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

GLOBAL_SENSOR_DESCRIPTIONS = (
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
)

CLIENT_SENSOR_DESCRIPTIONS = (
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
    hass: HomeAssistant,  # noqa: ARG001
    entry: AirplanesLiveConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    coordinator = entry.runtime_data.coordinator
    entities: list[SensorEntity] = []

    # Global sensors
    entities.extend(
        AirplanesLiveSensor(
            coordinator=coordinator,
            entity_description=entity_description,
        )
        for entity_description in GLOBAL_SENSOR_DESCRIPTIONS
    )

    # Beast Clients
    beast_clients = coordinator.data.get("beast_clients", [])
    for index, _ in enumerate(beast_clients):
        entities.extend(
            AirplanesLiveClientSensor(
                coordinator=coordinator,
                entity_description=entity_description,
                client_type="beast_clients",
                client_index=index,
            )
            for entity_description in CLIENT_SENSOR_DESCRIPTIONS
        )

    # MLAT Clients
    mlat_clients = coordinator.data.get("mlat_clients", [])
    for index, _ in enumerate(mlat_clients):
        entities.extend(
            AirplanesLiveClientSensor(
                coordinator=coordinator,
                entity_description=entity_description,
                client_type="mlat_clients",
                client_index=index,
            )
            for entity_description in CLIENT_SENSOR_DESCRIPTIONS
        )

    async_add_entities(entities)


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
        return self.coordinator.data.get(self.entity_description.key)


class AirplanesLiveClientSensor(AirplanesLiveEntity, SensorEntity):
    """Airplanes.live Client Sensor class."""

    def __init__(
        self,
        coordinator: AirplanesLiveFeederStatusCoordinator,
        entity_description: SensorEntityDescription,
        client_type: str,
        client_index: int,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self.client_type = client_type
        self.client_index = client_index

        type_name = "Beast" if client_type == "beast_clients" else "MLAT"
        self._attr_name = f"{type_name} Client {client_index} {entity_description.name}"
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_{client_type}_{client_index}_{entity_description.key}"

    @property
    def native_value(self) -> str | float | None:
        """Return the native value of the sensor."""
        clients = self.coordinator.data.get(self.client_type, [])
        if len(clients) <= self.client_index:
            return 0

        return clients[self.client_index].get(self.entity_description.key)
