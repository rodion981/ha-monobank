"""Constants for the Monobank integration."""

DOMAIN = "monobank"

# API
API_BASE_URL = "https://api.monobank.ua"
API_TIMEOUT = 30
API_MAX_RETRIES = 3
API_RETRY_DELAY = 5  # seconds

# Update intervals (seconds) - defaults
DEFAULT_UPDATE_INTERVAL_ACCOUNTS = 60  # 1 minute for accounts
DEFAULT_UPDATE_INTERVAL_CURRENCY = 300  # 5 minutes for currency rates
MIN_UPDATE_INTERVAL_ACCOUNTS = 30  # Minimum 30 seconds
MIN_UPDATE_INTERVAL_CURRENCY = 60  # Minimum 1 minute

# API endpoints
ENDPOINT_CLIENT_INFO = "/personal/client-info"
ENDPOINT_CURRENCY = "/bank/currency"
ENDPOINT_STATEMENT = "/personal/statement/{account}/{from}/{to}"
ENDPOINT_WEBHOOK = "/personal/webhook"

# Configuration
CONF_API_TOKEN = "api_token"

# Options
CONF_UPDATE_INTERVAL_ACCOUNTS = "update_interval_accounts"
CONF_UPDATE_INTERVAL_CURRENCY = "update_interval_currency"
CONF_ENABLE_CURRENCY_SENSORS = "enable_currency_sensors"
CONF_ENABLE_JARS = "enable_jars"
CONF_WEBHOOK_ID = "webhook_id"

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
    "black": "Чорна",
    "white": "Біла",
    "platinum": "Platinum",
    "iron": "Iron",
    "fop": "ФОП",
    "yellow": "Жовта",
    "eAid": "єПідтримка",
    "diia": "Дія",
    "madeInUkraine": "Нац кешбеку",
}

# Sensor types
SENSOR_TYPE_ACCOUNT = "account"
SENSOR_TYPE_JAR = "jar"
SENSOR_TYPE_CURRENCY = "currency"

# Attribution
ATTRIBUTION = "Data provided by Monobank API"
