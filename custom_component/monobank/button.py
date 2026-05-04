"""Button platform for Monobank integration."""
from __future__ import annotations

import logging
import re

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import DeviceInfo

from .const import ATTRIBUTION, DOMAIN
from .coordinator import MonobankAccountCoordinator

_LOGGER = logging.getLogger(__name__)


def slugify(text: str) -> str:
    """Convert text to slug format for entity_id."""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '_', text)
    return text.strip('_')


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Monobank buttons from a config entry."""
    data = hass.data[DOMAIN][entry.entry_id]
    account_coordinator: MonobankAccountCoordinator = data["account_coordinator"]

    # Get user name from coordinator data
    user_name = account_coordinator.data.get("name", "Monobank")
    user_slug = slugify(user_name.split()[0] if user_name else "monobank")

    entities: list[ButtonEntity] = [
        MonobankRefreshButton(account_coordinator, entry, user_slug)
    ]

    async_add_entities(entities)


class MonobankRefreshButton(CoordinatorEntity, ButtonEntity):
    """Representation of Monobank refresh button."""

    _attr_attribution = ATTRIBUTION

    def __init__(
        self,
        coordinator: MonobankAccountCoordinator,
        entry: ConfigEntry,
        user_slug: str,
    ) -> None:
        """Initialize the button."""
        super().__init__(coordinator)
        self._entry_id = entry.entry_id

        # Get user name and client_id for device info
        user_name = coordinator.data.get("name", "Monobank User")
        client_id = coordinator.data.get("client_id", entry.entry_id)

        # Set unique ID
        self._attr_unique_id = f"{entry.entry_id}_refresh"
        self._attr_name = "Оновити дані"
        self._attr_icon = "mdi:refresh"

        # Set entity_id suggestion: button.mono_rodion_refresh
        self.entity_id = f"button.mono_{user_slug}_refresh"

        # Device info - main device (hub)
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, client_id)},
            name=f"Monobank - {user_name}",
            manufacturer="Monobank",
            model="Personal Account",
            entry_type="service",
        )

    async def async_press(self) -> None:
        """Handle the button press."""
        _LOGGER.info("Manual refresh triggered")
        await self.coordinator.async_request_refresh()
