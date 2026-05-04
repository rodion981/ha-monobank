# Monobank Integration for Home Assistant

Кастомна інтеграція Monobank для Home Assistant, яка дозволяє відстежувати баланси рахунків, банок (цілей) та курси валют.

[English version below](#english-version)

## Українська версія

### Можливості

- 💳 **Рахунки**: Відстеження балансу всіх ваших карток Monobank
- 🏦 **Банки (Цілі)**: Моніторинг прогресу накопичень у банках
- 💱 **Курси валют**: Актуальні курси USD, EUR, GBP та інших валют
- 🔄 **Автоматичне оновлення**: Дані оновлюються кожні 60 секунд для рахунків та 5 хвилин для курсів
- 🌐 **Локалізація**: Підтримка української та англійської мов
- ⚙️ **UI конфігурація**: Проста настройка через інтерфейс Home Assistant

### Встановлення

#### Метод 1: HACS (рекомендовано)

1. Відкрийте HACS в Home Assistant
2. Перейдіть в розділ "Integrations"
3. Натисніть на три крапки в правому верхньому куті
4. Виберіть "Custom repositories"
5. Додайте URL цього репозиторію
6. Категорія: Integration
7. Знайдіть "Monobank" в списку та встановіть

#### Метод 2: Ручне встановлення

1. Скопіюйте папку `custom_components/monobank` в папку `custom_components` вашого Home Assistant
2. Перезапустіть Home Assistant

### Налаштування

1. Отримайте API токен на https://api.monobank.ua/
2. В Home Assistant перейдіть в **Settings** → **Devices & Services**
3. Натисніть **+ Add Integration**
4. Знайдіть **Monobank**
5. Введіть ваш API токен
6. Натисніть **Submit**

### Сенсори

Після налаштування інтеграція створить наступні сенсори:

#### Рахунки
- `sensor.monobank_black_xxxx` - Баланс чорної картки
- `sensor.monobank_white_xxxx` - Баланс білої картки
- `sensor.monobank_diia_xxxx` - Баланс картки Дія
- та інші...

**Атрибути:**
- `currency` - Валюта рахунку
- `card_type` - Тип картки
- `masked_pan` - Маскований номер картки
- `iban` - IBAN рахунку
- `credit_limit` - Кредитний ліміт
- `cashback_type` - Тип кешбеку

#### Банки (Цілі)
- `sensor.monobank_jar_название` - Баланс банки

**Атрибути:**
- `title` - Назва банки
- `description` - Опис
- `goal` - Ціль накопичення
- `progress` - Прогрес у відсотках
- `currency` - Валюта

#### Курси валют
- `sensor.monobank_usd_uah` - Курс долара
- `sensor.monobank_eur_uah` - Курс євро
- `sensor.monobank_gbp_uah` - Курс фунта

**Атрибути:**
- `rate_buy` - Курс купівлі
- `rate_sell` - Курс продажу
- `last_update` - Час останнього оновлення

### Приклади використання

#### Lovelace картка для відображення балансу

```yaml
type: entities
title: Мої рахунки Monobank
entities:
  - entity: sensor.monobank_black_1199
    name: Чорна картка
  - entity: sensor.monobank_white_8944
    name: Біла картка
```

#### Картка з курсами валют

```yaml
type: entities
title: Курси валют
entities:
  - entity: sensor.monobank_usd_uah
    name: USD
    secondary_info: last-updated
  - entity: sensor.monobank_eur_uah
    name: EUR
    secondary_info: last-updated
```

#### Автоматизація при низькому балансі

```yaml
automation:
  - alias: "Сповіщення про низький баланс"
    trigger:
      - platform: numeric_state
        entity_id: sensor.monobank_black_1199
        below: 100
    action:
      - service: notify.mobile_app
        data:
          message: "Баланс на чорній картці менше 100 грн!"
```

#### Автоматизація при досягненні цілі в банці

```yaml
automation:
  - alias: "Ціль досягнута"
    trigger:
      - platform: template
        value_template: "{{ state_attr('sensor.monobank_jar_3d_printer', 'progress') >= 100 }}"
    action:
      - service: notify.mobile_app
        data:
          message: "Вітаємо! Ви досягли цілі накопичення!"
```

### Обмеження API

Monobank API має наступні обмеження:
- Максимум 60 запитів на хвилину
- Інтеграція автоматично дотримується цих обмежень

### Структура файлів

```
custom_components/monobank/
├── __init__.py           # Ініціалізація інтеграції
├── manifest.json         # Метадані
├── config_flow.py        # UI конфігурація
├── const.py              # Константи
├── coordinator.py        # Координатор оновлення даних
├── sensor.py             # Сенсори
├── api.py                # API клієнт
├── strings.json          # Переклади
└── translations/
    ├── en.json           # Англійська локалізація
    └── uk.json           # Українська локалізація
```

### Підтримка

Якщо у вас виникли проблеми або є пропозиції, створіть issue в цьому репозиторії.

### Ліцензія

MIT License

---

## English Version

### Features

- 💳 **Accounts**: Track balances of all your Monobank cards
- 🏦 **Jars (Goals)**: Monitor savings progress in jars
- 💱 **Currency Rates**: Current rates for USD, EUR, GBP and other currencies
- 🔄 **Auto-update**: Data refreshes every 60 seconds for accounts and 5 minutes for rates
- 🌐 **Localization**: Ukrainian and English language support
- ⚙️ **UI Configuration**: Easy setup through Home Assistant interface

### Installation

#### Method 1: HACS (recommended)

1. Open HACS in Home Assistant
2. Go to "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add this repository URL
6. Category: Integration
7. Find "Monobank" in the list and install

#### Method 2: Manual Installation

1. Copy the `custom_components/monobank` folder to your Home Assistant `custom_components` folder
2. Restart Home Assistant

### Configuration

1. Get your API token from https://api.monobank.ua/
2. In Home Assistant go to **Settings** → **Devices & Services**
3. Click **+ Add Integration**
4. Search for **Monobank**
5. Enter your API token
6. Click **Submit**

### Sensors

After configuration, the integration will create the following sensors:

#### Accounts
- `sensor.monobank_black_xxxx` - Black card balance
- `sensor.monobank_white_xxxx` - White card balance
- `sensor.monobank_diia_xxxx` - Diia card balance
- and others...

**Attributes:**
- `currency` - Account currency
- `card_type` - Card type
- `masked_pan` - Masked card number
- `iban` - Account IBAN
- `credit_limit` - Credit limit
- `cashback_type` - Cashback type

#### Jars (Goals)
- `sensor.monobank_jar_name` - Jar balance

**Attributes:**
- `title` - Jar name
- `description` - Description
- `goal` - Savings goal
- `progress` - Progress percentage
- `currency` - Currency

#### Currency Rates
- `sensor.monobank_usd_uah` - USD rate
- `sensor.monobank_eur_uah` - EUR rate
- `sensor.monobank_gbp_uah` - GBP rate

**Attributes:**
- `rate_buy` - Buy rate
- `rate_sell` - Sell rate
- `last_update` - Last update time

### Usage Examples

#### Lovelace card for balance display

```yaml
type: entities
title: My Monobank Accounts
entities:
  - entity: sensor.monobank_black_1199
    name: Black Card
  - entity: sensor.monobank_white_8944
    name: White Card
```

#### Currency rates card

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

#### Low balance automation

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

#### Goal reached automation

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

### API Limitations

Monobank API has the following limitations:
- Maximum 60 requests per minute
- The integration automatically respects these limits

### Support

If you encounter any issues or have suggestions, please create an issue in this repository.

### License

MIT License
