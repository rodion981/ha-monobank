"""Options flow for Monobank integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry, OptionsFlow
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult

from .const import (
    CONF_ENABLE_CURRENCY_SENSORS,
    CONF_ENABLE_JARS,
    CONF_UPDATE_INTERVAL_ACCOUNTS,
    CONF_UPDATE_INTERVAL_CURRENCY,
    DEFAULT_UPDATE_INTERVAL_ACCOUNTS,
    DEFAULT_UPDATE_INTERVAL_CURRENCY,
    MIN_UPDATE_INTERVAL_ACCOUNTS,
    MIN_UPDATE_INTERVAL_CURRENCY,
)

_LOGGER = logging.getLogger(__name__)


class MonobankOptionsFlowHandler(OptionsFlow):
    """Handle Monobank options."""

    def __init__(self, config_entry: ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_UPDATE_INTERVAL_ACCOUNTS,
                        default=self.config_entry.options.get(
                            CONF_UPDATE_INTERVAL_ACCOUNTS,
                            DEFAULT_UPDATE_INTERVAL_ACCOUNTS,
                        ),
                    ): vol.All(
                        vol.Coerce(int),
                        vol.Range(min=MIN_UPDATE_INTERVAL_ACCOUNTS, max=3600),
                    ),
                    vol.Optional(
                        CONF_UPDATE_INTERVAL_CURRENCY,
                        default=self.config_entry.options.get(
                            CONF_UPDATE_INTERVAL_CURRENCY,
                            DEFAULT_UPDATE_INTERVAL_CURRENCY,
                        ),
                    ): vol.All(
                        vol.Coerce(int),
                        vol.Range(min=MIN_UPDATE_INTERVAL_CURRENCY, max=3600),
                    ),
                    vol.Optional(
                        CONF_ENABLE_CURRENCY_SENSORS,
                        default=self.config_entry.options.get(
                            CONF_ENABLE_CURRENCY_SENSORS, True
                        ),
                    ): bool,
                    vol.Optional(
                        CONF_ENABLE_JARS,
                        default=self.config_entry.options.get(CONF_ENABLE_JARS, True),
                    ): bool,
                }
            ),
        )
