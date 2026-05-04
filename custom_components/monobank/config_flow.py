"""Config flow for Monobank integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import MonobankAPI, MonobankAuthError, MonobankAPIError
from .const import CONF_API_TOKEN, DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_API_TOKEN): str,
    }
)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect.
    
    Args:
        hass: Home Assistant instance
        data: User input data
        
    Returns:
        Dictionary with client info
        
    Raises:
        MonobankAuthError: If authentication fails
        MonobankAPIError: If API request fails
    """
    session = async_get_clientsession(hass)
    api = MonobankAPI(data[CONF_API_TOKEN], session)

    try:
        # Validate token and get client info
        client_info = await api.get_client_info()
        
        return {
            "title": client_info.get("name", "Monobank"),
            "client_id": client_info.get("clientId"),
        }
    finally:
        # Don't close session as it's shared
        pass


class MonobankConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Monobank."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
            except MonobankAuthError:
                errors["base"] = "invalid_auth"
            except MonobankAPIError:
                errors["base"] = "cannot_connect"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                # Check if already configured
                await self.async_set_unique_id(info["client_id"])
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=info["title"],
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )
