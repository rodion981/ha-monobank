# Monobank Integration for Home Assistant

Кастомна інтеграція Monobank для Home Assistant, яка дозволяє відстежувати баланси рахунків, банок (цілей) та курси валют.

[English version below](#english-version)

## Українська версія

### Можливості

- 💳 **Рахунки**: Відстеження балансу всіх ваших карток Monobank
- 🏦 **Банки (Цілі)**: Моніторинг прогресу накопичень у банках
- 💱 **Курси валют**: Актуальні курси USD, EUR, GBP та інших валют
- 🔄 **Автоматичне оновлення**: Налаштовувані інтервали оновлення (за замовчуванням 60 сек для рахунків, 5 хв для курсів)
- 🔔 **Webhook підтримка**: Миттєві оновлення при транзакціях (опціонально)
- 🔘 **Ручне оновлення**: Кнопка для примусового оновлення даних
- 📊 **Статус API**: Сенсор для моніторингу доступності API
- ⚙️ **Налаштування через UI**: Повна конфігурація через інтерфейс Home Assistant
- 🎛️ **Feature toggles**: Можливість вимкнути сенсори валют або банок
- 🌐 **Локалізація**: Підтримка української та англійської мов
- 🔁 **Retry логіка**: Автоматичні повторні спроби при помилках API
- 🛡️ **Надійність**: Graceful обробка помилок та rate limits

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

#### Початкова конфігурація

1. Отримайте API токен на https://api.monobank.ua/
2. В Home Assistant перейдіть в **Settings** → **Devices & Services**
3. Натисніть **+ Add Integration**
4. Знайдіть **Monobank**
5. Введіть ваш API токен
6. Натисніть **Submit**

#### Додаткові налаштування (Options)

Після встановлення ви можете налаштувати інтеграцію:

1. Перейдіть в **Settings** → **Devices & Services**
2. Знайдіть **Monobank** та натисніть **Configure**
3. Доступні опції:
   - **Інтервал оновлення рахунків** (30-3600 сек, за замовчуванням 60)
   - **Інтервал оновлення курсів валют** (60-3600 сек, за замовчуванням 300)
   - **Увімкнути сенсори курсів валют** (так/ні)
   - **Увімкнути сенсори банок** (так/ні)

### Сенсори

Після налаштування інтеграція створить наступні сенсори:

#### Рахунки
- `sensor.monobank_black_xxxx` - Баланс чорної картки
- `sensor.monobank_white_xxxx` - Баланс білої картки
- `sensor.monobank_diia_xxxx` - Баланс картки Дія
- `sensor.monobank_eaid_xxxx` - Баланс картки єПідтримка
- `sensor.monobank_madeinukraine_xxxx` - Баланс картки Made in Ukraine
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

#### Статус API
- `binary_sensor.monobank_api_status` - Статус доступності API

**Атрибути:**
- `last_update_success` - Чи успішне останнє оновлення
- `last_error` - Текст останньої помилки (якщо є)
- `last_success_time` - Час останнього успішного оновлення

#### Кнопки
- `button.monobank_refresh` - Кнопка для ручного оновлення даних

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
  - entity: binary_sensor.monobank_api_status
    name: Статус API
  - entity: button.monobank_refresh
    name: Оновити дані
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

#### Автоматизація при помилці API

```yaml
automation:
  - alias: "Monobank API недоступний"
    trigger:
      - platform: state
        entity_id: binary_sensor.monobank_api_status
        to: "off"
        for:
          minutes: 5
    action:
      - service: notify.mobile_app
        data:
          message: "Monobank API недоступний більше 5 хвилин!"
```

### Webhook підтримка

Інтеграція автоматично реєструє webhook для отримання миттєвих оновлень від Monobank API. Webhook URL автоматично реєструється при встановленні інтеграції.

**Переваги webhook:**
- Миттєві оновлення при транзакціях
- Зменшення навантаження на API
- Більш актуальні дані

**Примітка:** Webhook працює паралельно з polling, тому дані будуть оновлюватись як при транзакціях, так і за розкладом.

### Обмеження API

Monobank API має наступні обмеження:
- Максимум 60 запитів на хвилину
- Інтеграція автоматично дотримується цих обмежень
- При перевищенні ліміту інтеграція автоматично повторює запити з затримкою

### Безпека

- API токен зберігається в зашифрованому вигляді
- Webhook використовує унікальний ID для кожної інсталяції
- Всі з'єднання використовують HTTPS
- Токен ніколи не логується в відкритому вигляді

### Структура файлів

```
custom_components/monobank/
├── __init__.py           # Ініціалізація інтеграції
├── manifest.json         # Метадані
├── config_flow.py        # UI конфігурація
├── options_flow.py       # UI налаштувань
├── const.py              # Константи
├── coordinator.py        # Координатор оновлення даних
├── sensor.py             # Сенсори
├── binary_sensor.py      # Бінарні сенсори
├── button.py             # Кнопки
├── api.py                # API клієнт
├── webhook.py            # Webhook обробка
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
- 🔄 **Auto-update**: Configurable update intervals (default 60s for accounts, 5min for rates)
- 🔔 **Webhook support**: Instant updates on transactions (optional)
- 🔘 **Manual refresh**: Button to force data update
- 📊 **API Status**: Sensor to monitor API availability
- ⚙️ **UI Configuration**: Full configuration through Home Assistant interface
- 🎛️ **Feature toggles**: Ability to disable currency or jar sensors
- 🌐 **Localization**: Ukrainian and English language support
- 🔁 **Retry logic**: Automatic retries on API errors
- 🛡️ **Reliability**: Graceful error handling and rate limit management

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

#### Initial Setup

1. Get your API token from https://api.monobank.ua/
2. In Home Assistant go to **Settings** → **Devices & Services**
3. Click **+ Add Integration**
4. Search for **Monobank**
5. Enter your API token
6. Click **Submit**

#### Additional Settings (Options)

After installation, you can configure the integration:

1. Go to **Settings** → **Devices & Services**
2. Find **Monobank** and click **Configure**
3. Available options:
   - **Account update interval** (30-3600 sec, default 60)
   - **Currency update interval** (60-3600 sec, default 300)
   - **Enable currency rate sensors** (yes/no)
   - **Enable jar sensors** (yes/no)

### Sensors

After configuration, the integration will create the following sensors:

#### Accounts
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

#### API Status
- `binary_sensor.monobank_api_status` - API availability status

**Attributes:**
- `last_update_success` - Whether last update was successful
- `last_error` - Last error text (if any)
- `last_success_time` - Time of last successful update

#### Buttons
- `button.monobank_refresh` - Button to manually refresh data

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
  - entity: binary_sensor.monobank_api_status
    name: API Status
  - entity: button.monobank_refresh
    name: Refresh Data
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

#### API error automation

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

### Webhook Support

The integration automatically registers a webhook to receive instant updates from Monobank API. The webhook URL is automatically registered during integration setup.

**Webhook benefits:**
- Instant updates on transactions
- Reduced API load
- More up-to-date data

**Note:** Webhook works in parallel with polling, so data will be updated both on transactions and on schedule.

### API Limitations

Monobank API has the following limitations:
- Maximum 60 requests per minute
- The integration automatically respects these limits
- On rate limit exceeded, the integration automatically retries with delay

### Security

- API token is stored encrypted
- Webhook uses unique ID for each installation
- All connections use HTTPS
- Token is never logged in plain text

### Support

If you encounter any issues or have suggestions, please create an issue in this repository.

### License

MIT License
