"""The Monobank integration."""
from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import MonobankAPI
from .const import (
    CONF_API_TOKEN,
    CONF_ENABLE_CURRENCY_SENSORS,
    CONF_ENABLE_JARS,
    CONF_UPDATE_INTERVAL_ACCOUNTS,
    CONF_UPDATE_INTERVAL_CURRENCY,
    CONF_WEBHOOK_ID,
    DEFAULT_UPDATE_INTERVAL_ACCOUNTS,
    DEFAULT_UPDATE_INTERVAL_CURRENCY,
    DOMAIN,
)
from .coordinator import MonobankAccountCoordinator, MonobankCurrencyCoordinator
from .webhook import async_setup_webhook, async_unload_webhook

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.BINARY_SENSOR, Platform.BUTTON]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Monobank from a config entry."""
    session = async_get_clientsession(hass)
    api = MonobankAPI(entry.data[CONF_API_TOKEN], session)

    # Get update intervals from options or use defaults
    account_interval = entry.options.get(
        CONF_UPDATE_INTERVAL_ACCOUNTS, DEFAULT_UPDATE_INTERVAL_ACCOUNTS
    )
    currency_interval = entry.options.get(
        CONF_UPDATE_INTERVAL_CURRENCY, DEFAULT_UPDATE_INTERVAL_CURRENCY
    )

    # Create coordinators with configured intervals
    account_coordinator = MonobankAccountCoordinator(hass, api, account_interval)
    currency_coordinator = MonobankCurrencyCoordinator(hass, api, currency_interval)

    # Fetch initial data
    await account_coordinator.async_config_entry_first_refresh()
    await currency_coordinator.async_config_entry_first_refresh()

    # Set up webhook
    try:
        webhook_url = await async_setup_webhook(hass, entry)
        _LOGGER.info("Webhook URL: %s", webhook_url)
        
        # Register webhook with Monobank API
        try:
            await api.set_webhook(webhook_url)
            _LOGGER.info("Webhook registered with Monobank API")
        except Exception as err:  # pylint: disable=broad-except
            _LOGGER.warning("Failed to register webhook with Monobank API: %s", err)
    except Exception as err:  # pylint: disable=broad-except
        _LOGGER.warning("Failed to set up webhook: %s", err)

    # Store coordinators
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "api": api,
        "account_coordinator": account_coordinator,
        "currency_coordinator": currency_coordinator,
    }

    # Forward entry setup to platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Register update listener for options changes
    entry.async_on_unload(entry.add_update_listener(async_update_options))

    return True


async def async_update_options(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle options update."""
    _LOGGER.info("Options updated, reloading integration")
    
    # Get coordinators
    data = hass.data[DOMAIN][entry.entry_id]
    account_coordinator: MonobankAccountCoordinator = data["account_coordinator"]
    currency_coordinator: MonobankCurrencyCoordinator = data["currency_coordinator"]

    # Update intervals if changed
    account_interval = entry.options.get(
        CONF_UPDATE_INTERVAL_ACCOUNTS, DEFAULT_UPDATE_INTERVAL_ACCOUNTS
    )
    currency_interval = entry.options.get(
        CONF_UPDATE_INTERVAL_CURRENCY, DEFAULT_UPDATE_INTERVAL_CURRENCY
    )

    account_coordinator.update_interval_seconds(account_interval)
    currency_coordinator.update_interval_seconds(currency_interval)

    # Reload the config entry to apply feature toggles
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # Unload webhook
    await async_unload_webhook(hass, entry)
    
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        data = hass.data[DOMAIN].pop(entry.entry_id)
        await data["api"].close()

    return unload_ok
