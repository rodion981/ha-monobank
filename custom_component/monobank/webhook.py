"""Webhook support for Monobank integration."""
from __future__ import annotations

import logging
from typing import Any

from aiohttp import web

from homeassistant.components import webhook
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_entry_oauth2_flow

from .const import CONF_WEBHOOK_ID, DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_webhook(hass: HomeAssistant, entry: ConfigEntry) -> str:
    """Set up webhook for Monobank integration.
    
    Args:
        hass: Home Assistant instance
        entry: Config entry
        
    Returns:
        Webhook URL
    """
    webhook_id = entry.data.get(CONF_WEBHOOK_ID)
    
    if not webhook_id:
        # Generate new webhook ID
        webhook_id = webhook.async_generate_id()
        hass.config_entries.async_update_entry(
            entry, data={**entry.data, CONF_WEBHOOK_ID: webhook_id}
        )
    
    webhook.async_register(
        hass,
        DOMAIN,
        "Monobank",
        webhook_id,
        handle_webhook,
    )
    
    webhook_url = webhook.async_generate_url(hass, webhook_id)
    _LOGGER.info("Webhook registered: %s", webhook_url)
    
    return webhook_url


async def async_unload_webhook(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Unload webhook.
    
    Args:
        hass: Home Assistant instance
        entry: Config entry
    """
    webhook_id = entry.data.get(CONF_WEBHOOK_ID)
    if webhook_id:
        webhook.async_unregister(hass, webhook_id)
        _LOGGER.info("Webhook unregistered")


async def handle_webhook(
    hass: HomeAssistant, webhook_id: str, request: web.Request
) -> web.Response:
    """Handle webhook callback from Monobank.
    
    Args:
        hass: Home Assistant instance
        webhook_id: Webhook ID
        request: HTTP request
        
    Returns:
        HTTP response
    """
    try:
        data = await request.json()
        _LOGGER.debug("Webhook received: %s", data)
        
        # Find the config entry for this webhook
        entry = None
        for config_entry in hass.config_entries.async_entries(DOMAIN):
            if config_entry.data.get(CONF_WEBHOOK_ID) == webhook_id:
                entry = config_entry
                break
        
        if not entry:
            _LOGGER.error("Config entry not found for webhook %s", webhook_id)
            return web.Response(status=404)
        
        # Trigger coordinator refresh
        domain_data = hass.data[DOMAIN].get(entry.entry_id)
        if domain_data:
            account_coordinator = domain_data["account_coordinator"]
            _LOGGER.info("Webhook triggered, refreshing data")
            await account_coordinator.async_request_refresh()
        
        return web.Response(status=200)
        
    except Exception as err:  # pylint: disable=broad-except
        _LOGGER.exception("Error handling webhook: %s", err)
        return web.Response(status=500)
