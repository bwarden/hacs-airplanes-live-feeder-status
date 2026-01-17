"""Adds config flow for Airplanes.live Feeder Status."""

from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_create_clientsession

from .api import (
    AirplanesLiveApiClient,
    AirplanesLiveApiClientCommunicationError,
    AirplanesLiveApiClientError,
)
from .const import DOMAIN, LOGGER


class AirplanesLiveFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Airplanes.live Feeder Status."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict | None = None,
    ) -> config_entries.ConfigFlowResult:
        """Handle a flow initialized by the user."""
        _errors = {}
        if user_input is not None:
            try:
                await self._test_connection()
            except AirplanesLiveApiClientCommunicationError as exception:
                LOGGER.error(exception)
                _errors["base"] = "connection"
            except AirplanesLiveApiClientError as exception:
                LOGGER.exception(exception)
                _errors["base"] = "unknown"
            else:
                return self.async_create_entry(
                    title="Airplanes.live Feeder Status",
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({}),
            errors=_errors,
        )

    async def _test_connection(self) -> None:
        """Validate connection."""
        client = AirplanesLiveApiClient(
            session=async_create_clientsession(self.hass),
        )
        await client.async_get_data()
