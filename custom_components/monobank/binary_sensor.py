"""Binary sensor platform for Monobank integration."""
from __future__ import annotations

import logging
import re
from typing import Any

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import DeviceInfo, EntityCategory

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
    """Set up Monobank binary sensors from a config entry."""
    data = hass.data[DOMAIN][entry.entry_id]
    account_coordinator: MonobankAccountCoordinator = data["account_coordinator"]

    # Get user name from coordinator data
    user_name = account_coordinator.data.get("name", "Monobank")
    user_slug = slugify(user_name.split()[0] if user_name else "monobank")

    entities: list[BinarySensorEntity] = [
        MonobankAPIStatusSensor(account_coordinator, entry, user_slug)
    ]

    async_add_entities(entities)


class MonobankAPIStatusSensor(CoordinatorEntity, BinarySensorEntity):
    """Representation of Monobank API status sensor."""

    _attr_device_class = BinarySensorDeviceClass.CONNECTIVITY
    _attr_attribution = ATTRIBUTION
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MonobankAccountCoordinator,
        entry: ConfigEntry,
        user_slug: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._entry_id = entry.entry_id
        self._attr_available = True  # Always available

        # Get user name and client_id for device info
        user_name = coordinator.data.get("name", "Monobank User")
        client_id = coordinator.data.get("client_id", entry.entry_id)

        # Set unique ID
        self._attr_unique_id = f"{entry.entry_id}_api_status"
        self._attr_name = "Статус API"

        # Set entity_id suggestion: binary_sensor.mono_rodion_api_status
        self.entity_id = f"binary_sensor.mono_{user_slug}_api_status"

        # Entity category - Налаштування (CONFIG)
        self._attr_entity_category = EntityCategory.CONFIG

        # Device info - main device (hub)
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, client_id)},
            name=f"Monobank - {user_name}",
            manufacturer="Monobank",
            model="Personal Account",
            entry_type="service",
        )

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

        # Use last_update_success_time if available, otherwise use last_update_time
        if hasattr(self.coordinator, "last_update_success_time") and self.coordinator.last_update_success_time:
            attributes["last_success_time"] = self.coordinator.last_update_success_time.isoformat()
        elif self.coordinator.last_update_success and hasattr(self.coordinator, "last_update_time") and self.coordinator.last_update_time:
            attributes["last_success_time"] = self.coordinator.last_update_time.isoformat()

        return attributes

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        # Always remain available
        self._attr_available = True
        self.async_write_ha_state()

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        # This sensor should always be available to show API status
        return True
