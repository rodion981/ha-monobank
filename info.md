# Monobank Integration for Home Assistant

Кастомна інтеграція Monobank для Home Assistant.

## Можливості

- 💳 **Рахунки**: Відстеження балансу всіх ваших карток Monobank
- 🏦 **Банки (Цілі)**: Моніторинг прогресу накопичень у банках
- 💱 **Курси валют**: Актуальні курси USD, EUR, GBP та інших валют
- 🔄 **Автоматичне оновлення**: Налаштовувані інтервали оновлення
- 🔔 **Webhook підтримка**: Миттєві оновлення при транзакціях
- 🔘 **Ручне оновлення**: Кнопка для примусового оновлення даних
- 📊 **Статус API**: Сенсор для моніторингу доступності API
- ⚙️ **Налаштування через UI**: Повна конфігурація через інтерфейс Home Assistant

## Встановлення

### Через HACS (рекомендовано)

1. Відкрийте HACS в Home Assistant
2. Перейдіть в розділ "Integrations"
3. Натисніть на три крапки в правому верхньому куті
4. Виберіть "Custom repositories"
5. Додайте URL: `https://github.com/rodion981/ha-monobank`
6. Категорія: Integration
7. Знайдіть "Monobank" в списку та встановіть
8. Перезапустіть Home Assistant

### Ручне встановлення

1. Скопіюйте папку `custom_components/monobank` в папку `config/custom_components/` вашого Home Assistant
2. Перезапустіть Home Assistant

## Налаштування

1. Отримайте API токен на https://api.monobank.ua/
2. В Home Assistant перейдіть в **Settings** → **Devices & Services**
3. Натисніть **+ Add Integration**
4. Знайдіть **Monobank**
5. Введіть ваш API токен
6. Натисніть **Submit**

## Документація

Повна документація доступна в [README.md](https://github.com/rodion981/ha-monobank/blob/main/README.md)
