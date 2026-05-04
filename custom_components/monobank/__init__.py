"""The Monobank integration."""
from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import MonobankAPI
from .const import CONF_API_TOKEN, DOMAIN
from .coordinator import MonobankAccountCoordinator, MonobankCurrencyCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Monobank from a config entry."""
    session = async_get_clientsession(hass)
    api = MonobankAPI(entry.data[CONF_API_TOKEN], session)

    # Create coordinators
    account_coordinator = MonobankAccountCoordinator(hass, api)
    currency_coordinator = MonobankCurrencyCoordinator(hass, api)

    # Fetch initial data
    await account_coordinator.async_config_entry_first_refresh()
    await currency_coordinator.async_config_entry_first_refresh()

    # Store coordinators
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "api": api,
        "account_coordinator": account_coordinator,
        "currency_coordinator": currency_coordinator,
    }

    # Forward entry setup to platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        data = hass.data[DOMAIN].pop(entry.entry_id)
        await data["api"].close()

    return unload_ok
