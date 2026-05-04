"""Button platform for Monobank integration."""
from __future__ import annotations

import logging

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import ATTRIBUTION, DOMAIN
from .coordinator import MonobankAccountCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Monobank buttons from a config entry."""
    data = hass.data[DOMAIN][entry.entry_id]
    account_coordinator: MonobankAccountCoordinator = data["account_coordinator"]

    entities: list[ButtonEntity] = [
        MonobankRefreshButton(account_coordinator, entry)
    ]

    async_add_entities(entities)


class MonobankRefreshButton(CoordinatorEntity, ButtonEntity):
    """Representation of Monobank refresh button."""

    _attr_attribution = ATTRIBUTION

    def __init__(
        self,
        coordinator: MonobankAccountCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the button."""
        super().__init__(coordinator)
        self._entry_id = entry.entry_id

        # Set unique ID
        self._attr_unique_id = f"{entry.entry_id}_refresh"
        self._attr_name = "Monobank Refresh"
        self._attr_icon = "mdi:refresh"

    async def async_press(self) -> None:
        """Handle the button press."""
        _LOGGER.info("Manual refresh triggered")
        await self.coordinator.async_request_refresh()
