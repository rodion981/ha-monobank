"""Binary sensor platform for Monobank integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
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
    """Set up Monobank binary sensors from a config entry."""
    data = hass.data[DOMAIN][entry.entry_id]
    account_coordinator: MonobankAccountCoordinator = data["account_coordinator"]

    entities: list[BinarySensorEntity] = [
        MonobankAPIStatusSensor(account_coordinator, entry)
    ]

    async_add_entities(entities)


class MonobankAPIStatusSensor(CoordinatorEntity, BinarySensorEntity):
    """Representation of Monobank API status sensor."""

    _attr_device_class = BinarySensorDeviceClass.CONNECTIVITY
    _attr_attribution = ATTRIBUTION

    def __init__(
        self,
        coordinator: MonobankAccountCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._entry_id = entry.entry_id

        # Set unique ID
        self._attr_unique_id = f"{entry.entry_id}_api_status"
        self._attr_name = "Monobank API Status"

    @property
    def is_on(self) -> bool:
        """Return true if API is available."""
        return self.coordinator.last_update_success

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        attributes = {
            "last_update_success": self.coordinator.last_update_success,
        }

        if self.coordinator.last_exception:
            attributes["last_error"] = str(self.coordinator.last_exception)

        if self.coordinator.last_update_success_time:
            attributes["last_success_time"] = self.coordinator.last_update_success_time.isoformat()

        return attributes

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        # This sensor should always be available to show API status
        return True
