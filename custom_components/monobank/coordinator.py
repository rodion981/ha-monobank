"""DataUpdateCoordinator for Monobank."""
from __future__ import annotations

from datetime import timedelta
import logging
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import MonobankAPI, MonobankAPIError, MonobankRateLimitError
from .const import (
    DOMAIN,
    DEFAULT_UPDATE_INTERVAL_ACCOUNTS,
    DEFAULT_UPDATE_INTERVAL_CURRENCY,
)

_LOGGER = logging.getLogger(__name__)


class MonobankCoordinator(DataUpdateCoordinator):
    """Monobank data update coordinator."""

    def __init__(
        self,
        hass: HomeAssistant,
        api: MonobankAPI,
        update_interval: int,
    ) -> None:
        """Initialize coordinator.
        
        Args:
            hass: Home Assistant instance
            api: Monobank API client
            update_interval: Update interval in seconds
        """
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=update_interval),
        )
        self.api = api
        self._update_interval_seconds = update_interval

    def update_interval_seconds(self, interval: int) -> None:
        """Update the polling interval.
        
        Args:
            interval: New interval in seconds
        """
        self._update_interval_seconds = interval
        self.update_interval = timedelta(seconds=interval)
        _LOGGER.info("Update interval changed to %d seconds", interval)

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from API."""
        raise NotImplementedError


class MonobankAccountCoordinator(MonobankCoordinator):
    """Coordinator for account and jar data."""

    def __init__(self, hass: HomeAssistant, api: MonobankAPI, update_interval: int | None = None) -> None:
        """Initialize account coordinator."""
        super().__init__(hass, api, update_interval or DEFAULT_UPDATE_INTERVAL_ACCOUNTS)

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch account and jar data from API.
        
        Returns:
            Dictionary with accounts and jars data
        """
        try:
            _LOGGER.debug("Fetching account and jar data")
            data = await self.api.get_client_info()
            
            return {
                "client_id": data.get("clientId"),
                "name": data.get("name"),
                "accounts": data.get("accounts", []),
                "jars": data.get("jars", []),
            }

        except MonobankRateLimitError as err:
            _LOGGER.warning("Rate limit exceeded, will retry later: %s", err)
            raise UpdateFailed(f"Rate limit exceeded: {err}") from err
        except MonobankAPIError as err:
            _LOGGER.error("Error fetching account data: %s", err)
            raise UpdateFailed(f"Error fetching data: {err}") from err


class MonobankCurrencyCoordinator(MonobankCoordinator):
    """Coordinator for currency rates data."""

    def __init__(self, hass: HomeAssistant, api: MonobankAPI, update_interval: int | None = None) -> None:
        """Initialize currency coordinator."""
        super().__init__(hass, api, update_interval or DEFAULT_UPDATE_INTERVAL_CURRENCY)

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch currency rates from API.
        
        Returns:
            Dictionary with currency rates indexed by currency pair
        """
        try:
            _LOGGER.debug("Fetching currency rates")
            rates = await self.api.get_currency_rates()
            
            # Index rates by currency pair for easy lookup
            rates_dict = {}
            for rate in rates:
                currency_a = rate.get("currencyCodeA")
                currency_b = rate.get("currencyCodeB")
                key = f"{currency_a}_{currency_b}"
                rates_dict[key] = rate
            
            return rates_dict

        except MonobankRateLimitError as err:
            _LOGGER.warning("Rate limit exceeded, will retry later: %s", err)
            raise UpdateFailed(f"Rate limit exceeded: {err}") from err
        except MonobankAPIError as err:
            _LOGGER.error("Error fetching currency data: %s", err)
            raise UpdateFailed(f"Error fetching data: {err}") from err
