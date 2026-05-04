"""Constants for the Monobank integration."""

DOMAIN = "monobank"

# API
API_BASE_URL = "https://api.monobank.ua"
API_TIMEOUT = 30

# Update intervals (seconds)
UPDATE_INTERVAL_ACCOUNTS = 60  # 1 minute for accounts
UPDATE_INTERVAL_CURRENCY = 300  # 5 minutes for currency rates

# API endpoints
ENDPOINT_CLIENT_INFO = "/personal/client-info"
ENDPOINT_CURRENCY = "/bank/currency"
ENDPOINT_STATEMENT = "/personal/statement/{account}/{from}/{to}"

# Configuration
CONF_API_TOKEN = "api_token"

# Currency codes (ISO 4217)
CURRENCY_CODES = {
    980: "UAH",
    840: "USD",
    978: "EUR",
    826: "GBP",
    985: "PLN",
    203: "CZK",
    756: "CHF",
    392: "JPY",
    156: "CNY",
}

# Popular currency pairs for sensors
DEFAULT_CURRENCY_PAIRS = [
    (840, 980),  # USD/UAH
    (978, 980),  # EUR/UAH
    (826, 980),  # GBP/UAH
]

# Card types
CARD_TYPES = {
    "black": "Black",
    "white": "White",
    "platinum": "Platinum",
    "iron": "Iron",
    "fop": "FOP",
    "yellow": "Yellow",
    "eAid": "єПідтримка",
    "diia": "Дія",
    "madeInUkraine": "Made in Ukraine",
}

# Sensor types
SENSOR_TYPE_ACCOUNT = "account"
SENSOR_TYPE_JAR = "jar"
SENSOR_TYPE_CURRENCY = "currency"

# Attribution
ATTRIBUTION = "Data provided by Monobank API"
