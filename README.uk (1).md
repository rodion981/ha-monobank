# Monobank Integration for Home Assistant

[English](./README.md) | [**Українською**](./README.uk.md)

Кастомна інтеграція Monobank для Home Assistant, яка дозволяє відстежувати баланси рахунків, банок (цілей) та курси валют.

### Можливості

- 💳 **Рахунки**: Відстеження балансу всіх ваших карток Monobank
- 🏦 **Банки (Цілі)**: Моніторинг прогресу накопичень у банках
- 💱 **Курси валют**: Актуальні курси USD, EUR, GBP та інших валют
- 🔄 **Автоматичне оновлення**: Налаштовувані інтервали оновлення (за замовчуванням 60 сек для рахунків, 5 хв для курсів)
- 🔔 **Webhook підтримка**: Миттєві оновлення при транзакціях (опціонально)
- 🔘 **Ручне оновлення**: Кнопка для примусового оновлення даних
- 📊 **Статус API**: Сенсор для моніторингу доступності API
- ⚙️ **Налаштування через UI**: Повна конфігурація через інтерфейс Home Assistant
- 🎛️ **Перемикачі функцій**: Можливість вимкнути сенсори валют або банок
- 🌐 **Локалізація**: Підтримка української та англійської мов
- 🔁 **Повторні спроби**: Автоматичні повторні спроби при помилках API
- 🛡️ **Надійність**: Коректна обробка помилок і лімітів API

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

1. Скопіюйте папку `custom_components/monobank` до папки `custom_components` вашого Home Assistant
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
- `sensor.monobank_jar_name` - Баланс банки

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

Інтеграція автоматично реєструє webhook для отримання миттєвих оновлень від Monobank API. Для його роботи Home Assistant повинен мати доступну з інтернету HTTPS-адресу.

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

- API-токен зберігається локально в config entry Home Assistant; захистіть доступ до системи та резервних копій
- Webhook використовує унікальний ID для кожної інсталяції
- Всі з'єднання використовують HTTPS
- Токен ніколи не логується у відкритому вигляді

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
