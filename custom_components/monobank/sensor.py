"""Sensor platform for Monobank integration."""
from __future__ import annotations

from datetime import datetime
import logging
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    ATTRIBUTION,
    CARD_TYPES,
    CURRENCY_CODES,
    DEFAULT_CURRENCY_PAIRS,
    DOMAIN,
    SENSOR_TYPE_ACCOUNT,
    SENSOR_TYPE_CURRENCY,
    SENSOR_TYPE_JAR,
)
from .coordinator import MonobankAccountCoordinator, MonobankCurrencyCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Monobank sensors from a config entry."""
    data = hass.data[DOMAIN][entry.entry_id]
    account_coordinator: MonobankAccountCoordinator = data["account_coordinator"]
    currency_coordinator: MonobankCurrencyCoordinator = data["currency_coordinator"]

    entities: list[SensorEntity] = []

    # Create account sensors
    for account in account_coordinator.data.get("accounts", []):
        entities.append(MonobankAccountSensor(account_coordinator, account, entry))

    # Create jar sensors
    for jar in account_coordinator.data.get("jars", []):
        entities.append(MonobankJarSensor(account_coordinator, jar, entry))

    # Create currency sensors for default pairs
    for currency_a, currency_b in DEFAULT_CURRENCY_PAIRS:
        key = f"{currency_a}_{currency_b}"
        if key in currency_coordinator.data:
            entities.append(
                MonobankCurrencySensor(
                    currency_coordinator, currency_a, currency_b, entry
                )
            )

    async_add_entities(entities)


class MonobankAccountSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Monobank account sensor."""

    _attr_device_class = SensorDeviceClass.MONETARY
    _attr_state_class = SensorStateClass.TOTAL
    _attr_attribution = ATTRIBUTION

    def __init__(
        self,
        coordinator: MonobankAccountCoordinator,
        account: dict[str, Any],
        entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._account_id = account["id"]
        self._entry_id = entry.entry_id

        # Set unique ID
        self._attr_unique_id = f"{entry.entry_id}_{self._account_id}"

        # Set currency
        currency_code = account.get("currencyCode", 980)
        self._attr_native_unit_of_measurement = CURRENCY_CODES.get(
            currency_code, "UAH"
        )

        # Set name
        card_type = CARD_TYPES.get(account.get("type", ""), account.get("type", ""))
        masked_pan = account.get("maskedPan", [""])[0]
        self._attr_name = f"Monobank {card_type} {masked_pan[-4:]}"

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        account = self._get_account()
        if account is None:
            return None

        # Convert from cents/kopiykas to main currency unit
        balance = account.get("balance", 0)
        return balance / 100

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        account = self._get_account()
        if account is None:
            return {}

        currency_code = account.get("currencyCode", 980)
        credit_limit = account.get("creditLimit", 0) / 100

        attributes = {
            "account_id": account.get("id"),
            "currency": CURRENCY_CODES.get(currency_code, "UAH"),
            "currency_code": currency_code,
            "card_type": account.get("type"),
            "card_type_name": CARD_TYPES.get(account.get("type", ""), account.get("type", "")),
            "masked_pan": account.get("maskedPan", []),
            "iban": account.get("iban"),
            "cashback_type": account.get("cashbackType"),
            "credit_limit": credit_limit,
        }

        if account.get("sendId"):
            attributes["send_id"] = account.get("sendId")

        return attributes

    def _get_account(self) -> dict[str, Any] | None:
        """Get account data from coordinator."""
        for account in self.coordinator.data.get("accounts", []):
            if account["id"] == self._account_id:
                return account
        return None


class MonobankJarSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Monobank jar sensor."""

    _attr_device_class = SensorDeviceClass.MONETARY
    _attr_state_class = SensorStateClass.TOTAL
    _attr_attribution = ATTRIBUTION

    def __init__(
        self,
        coordinator: MonobankAccountCoordinator,
        jar: dict[str, Any],
        entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._jar_id = jar["id"]
        self._entry_id = entry.entry_id

        # Set unique ID
        self._attr_unique_id = f"{entry.entry_id}_jar_{self._jar_id}"

        # Set currency
        currency_code = jar.get("currencyCode", 980)
        self._attr_native_unit_of_measurement = CURRENCY_CODES.get(
            currency_code, "UAH"
        )

        # Set name
        jar_title = jar.get("title", "Jar")
        self._attr_name = f"Monobank Jar {jar_title}"

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        jar = self._get_jar()
        if jar is None:
            return None

        # Convert from cents/kopiykas to main currency unit
        balance = jar.get("balance", 0)
        return balance / 100

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        jar = self._get_jar()
        if jar is None:
            return {}

        currency_code = jar.get("currencyCode", 980)
        balance = jar.get("balance", 0) / 100
        goal = jar.get("goal", 0) / 100
        
        # Calculate progress percentage
        progress = 0
        if goal > 0:
            progress = round((balance / goal) * 100, 2)

        attributes = {
            "jar_id": jar.get("id"),
            "title": jar.get("title"),
            "description": jar.get("description"),
            "currency": CURRENCY_CODES.get(currency_code, "UAH"),
            "currency_code": currency_code,
            "goal": goal,
            "progress": progress,
        }

        if jar.get("sendId"):
            attributes["send_id"] = jar.get("sendId")

        return attributes

    def _get_jar(self) -> dict[str, Any] | None:
        """Get jar data from coordinator."""
        for jar in self.coordinator.data.get("jars", []):
            if jar["id"] == self._jar_id:
                return jar
        return None


class MonobankCurrencySensor(CoordinatorEntity, SensorEntity):
    """Representation of a Monobank currency rate sensor."""

    _attr_device_class = SensorDeviceClass.MONETARY
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_attribution = ATTRIBUTION

    def __init__(
        self,
        coordinator: MonobankCurrencyCoordinator,
        currency_a: int,
        currency_b: int,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._currency_a = currency_a
        self._currency_b = currency_b
        self._entry_id = entry.entry_id
        self._key = f"{currency_a}_{currency_b}"

        # Set unique ID
        self._attr_unique_id = f"{entry.entry_id}_currency_{self._key}"

        # Set currency
        self._attr_native_unit_of_measurement = CURRENCY_CODES.get(currency_b, "UAH")

        # Set name
        currency_a_name = CURRENCY_CODES.get(currency_a, str(currency_a))
        currency_b_name = CURRENCY_CODES.get(currency_b, str(currency_b))
        self._attr_name = f"Monobank {currency_a_name}/{currency_b_name}"

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        rate_data = self.coordinator.data.get(self._key)
        if rate_data is None:
            return None

        # Return average of buy and sell rates, or cross rate
        if "rateCross" in rate_data:
            return rate_data["rateCross"]
        
        rate_buy = rate_data.get("rateBuy", 0)
        rate_sell = rate_data.get("rateSell", 0)
        
        if rate_buy and rate_sell:
            return round((rate_buy + rate_sell) / 2, 4)
        
        return rate_buy or rate_sell or None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        rate_data = self.coordinator.data.get(self._key)
        if rate_data is None:
            return {}

        attributes = {
            "currency_a": CURRENCY_CODES.get(self._currency_a, str(self._currency_a)),
            "currency_b": CURRENCY_CODES.get(self._currency_b, str(self._currency_b)),
            "currency_a_code": self._currency_a,
            "currency_b_code": self._currency_b,
        }

        if "rateBuy" in rate_data:
            attributes["rate_buy"] = rate_data["rateBuy"]
        
        if "rateSell" in rate_data:
            attributes["rate_sell"] = rate_data["rateSell"]
        
        if "rateCross" in rate_data:
            attributes["rate_cross"] = rate_data["rateCross"]

        if "date" in rate_data:
            # Convert Unix timestamp to datetime
            timestamp = rate_data["date"]
            attributes["last_update"] = datetime.fromtimestamp(timestamp).isoformat()

        return attributes
