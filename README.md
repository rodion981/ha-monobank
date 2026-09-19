# Monobank

Bring Monobank accounts, jars, exchange rates, and API status into Home Assistant.

[![GitHub Release](https://img.shields.io/github/v/release/rodion981/ha-monobank?display_name=tag&sort=semver)](https://github.com/rodion981/ha-monobank/releases)
[![HACS](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://hacs.xyz/)
[![License](https://img.shields.io/github/license/rodion981/ha-monobank)](./LICENSE)

[**English**](./README.md) | [Українською](./README.uk.md)

## Quick install

1. Open this repository in HACS using the button below and download the integration.
2. Restart Home Assistant.
3. Use **Add Integration** to start the setup flow.

[![Open in HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=rodion981&repository=ha-monobank&category=integration)

[![Add Integration](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=monobank)

> [!NOTE]
> The HACS button requires HACS to be installed. The Add Integration button works after the custom integration has been downloaded and Home Assistant restarted.

Custom Monobank integration for Home Assistant that lets you track account balances, jars (goals), and currency exchange rates.


## Features

- 💳 **Accounts**: Track balances of all your Monobank cards
- 🏦 **Jars (Goals)**: Monitor savings progress in jars
- 💱 **Currency Rates**: Current rates for USD, EUR, GBP and other currencies
- 🔄 **Auto-update**: Configurable update intervals (default 60s for accounts, 5min for rates)
- 🔔 **Webhook support**: Automatic instant updates on transactions
- 🔘 **Manual refresh**: Button to force data update
- 📊 **API Status**: Sensor to monitor API availability
- ⚙️ **UI Configuration**: Full configuration through Home Assistant interface
- 🎛️ **Feature toggles**: Ability to disable currency or jar sensors
- 🌐 **Localization**: Ukrainian and English language support
- 🔁 **Retry logic**: Automatic retries on API errors
- 🛡️ **Reliability**: Graceful error handling and rate limit management

## Installation

### Method 1: HACS (recommended)

1. Open HACS in Home Assistant
2. Go to "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add this repository URL
6. Category: Integration
7. Find "Monobank" in the list and install

### Method 2: Manual Installation

1. Copy the `custom_components/monobank` folder to your Home Assistant `custom_components` folder
2. Restart Home Assistant

## Configuration

### Initial Setup

1. Get your API token from https://api.monobank.ua/
2. In Home Assistant go to **Settings** → **Devices & Services**
3. Click **+ Add Integration**
4. Search for **Monobank**
5. Enter your API token
6. Click **Submit**

### Additional Settings (Options)

After installation, you can configure the integration:

1. Go to **Settings** → **Devices & Services**
2. Find **Monobank** and click **Configure**
3. Available options:
   - **Account update interval** (30-3600 sec, default 60)
   - **Currency update interval** (60-3600 sec, default 300)
   - **Enable currency rate sensors** (yes/no)
   - **Enable jar sensors** (yes/no)

## Sensors

After configuration, the integration will create the following sensors:

### Accounts
- `sensor.monobank_black_xxxx` - Black card balance
- `sensor.monobank_white_xxxx` - White card balance
- `sensor.monobank_diia_xxxx` - Diia card balance
- `sensor.monobank_eaid_xxxx` - єПідтримка card balance
- `sensor.monobank_madeinukraine_xxxx` - Made in Ukraine card balance
- and others...

**Attributes:**
- `currency` - Account currency
- `card_type` - Card type
- `masked_pan` - Masked card number
- `iban` - Account IBAN
- `credit_limit` - Credit limit
- `cashback_type` - Cashback type

### Jars (Goals)
- `sensor.monobank_jar_name` - Jar balance

**Attributes:**
- `title` - Jar name
- `description` - Description
- `goal` - Savings goal
- `progress` - Progress percentage
- `currency` - Currency

### Currency Rates
- `sensor.monobank_usd_uah` - USD rate
- `sensor.monobank_eur_uah` - EUR rate
- `sensor.monobank_gbp_uah` - GBP rate

**Attributes:**
- `rate_buy` - Buy rate
- `rate_sell` - Sell rate
- `last_update` - Last update time

### API Status
- `binary_sensor.monobank_api_status` - API availability status

**Attributes:**
- `last_update_success` - Whether last update was successful
- `last_error` - Last error text (if any)
- `last_success_time` - Time of last successful update

### Buttons
- `button.monobank_refresh` - Button to manually refresh data

## Usage Examples

### Lovelace card for balance display

```yaml
type: entities
title: My Monobank Accounts
entities:
  - entity: sensor.monobank_black_1199
    name: Black Card
  - entity: sensor.monobank_white_8944
    name: White Card
  - entity: binary_sensor.monobank_api_status
    name: API Status
  - entity: button.monobank_refresh
    name: Refresh Data
```

### Currency rates card

```yaml
type: entities
title: Currency Rates
entities:
  - entity: sensor.monobank_usd_uah
    name: USD
    secondary_info: last-updated
  - entity: sensor.monobank_eur_uah
    name: EUR
    secondary_info: last-updated
```

### Low balance automation

```yaml
automation:
  - alias: "Low Balance Notification"
    trigger:
      - platform: numeric_state
        entity_id: sensor.monobank_black_1199
        below: 100
    action:
      - service: notify.mobile_app
        data:
          message: "Black card balance is below 100 UAH!"
```

### Goal reached automation

```yaml
automation:
  - alias: "Goal Reached"
    trigger:
      - platform: template
        value_template: "{{ state_attr('sensor.monobank_jar_3d_printer', 'progress') >= 100 }}"
    action:
      - service: notify.mobile_app
        data:
          message: "Congratulations! You've reached your savings goal!"
```

### API error automation

```yaml
automation:
  - alias: "Monobank API Unavailable"
    trigger:
      - platform: state
        entity_id: binary_sensor.monobank_api_status
        to: "off"
        for:
          minutes: 5
    action:
      - service: notify.mobile_app
        data:
          message: "Monobank API has been unavailable for more than 5 minutes!"
```

## Webhook Support

The integration automatically registers a webhook to receive instant updates from Monobank API. Home Assistant must have an internet-accessible HTTPS URL for it to work.

**Webhook benefits:**
- Instant updates on transactions
- Reduced API load
- More up-to-date data

**Note:** Webhook works in parallel with polling, so data will be updated both on transactions and on schedule.

## API Limitations

Monobank API has the following limitations:
- Maximum 60 requests per minute
- The integration automatically respects these limits
- On rate limit exceeded, the integration automatically retries with delay

## Security

- The API token is stored locally in the Home Assistant config entry; protect access to the system and its backups
- Webhook uses unique ID for each installation
- All connections use HTTPS
- Token is never logged in plain text


## File Structure

```text
custom_components/monobank/
├── __init__.py           # Integration initialization
├── manifest.json         # Metadata
├── config_flow.py        # UI configuration
├── options_flow.py       # UI options
├── const.py              # Constants
├── coordinator.py        # Data update coordinator
├── sensor.py             # Sensors
├── binary_sensor.py      # Binary sensors
├── button.py             # Buttons
├── api.py                # API client
├── webhook.py            # Webhook handling
├── strings.json          # Translations
└── translations/
    ├── en.json           # English localization
    └── uk.json           # Ukrainian localization
```

## Support

If you encounter any issues or have suggestions, please create an issue in this repository.

## License

MIT License
