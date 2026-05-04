# Інструкція по завантаженню на GitHub та встановленню в Home Assistant

## Крок 1: Створення репозиторію на GitHub

1. Перейдіть на https://github.com та увійдіть в свій акаунт
2. Натисніть на кнопку **"New"** (або **"+"** → **"New repository"**)
3. Заповніть форму:
   - **Repository name:** `monobank-homeassistant`
   - **Description:** `Monobank integration for Home Assistant`
   - **Public** (щоб можна було використовувати з HACS)
   - ✅ Add a README file - **НЕ ставте галочку** (у нас вже є README)
   - ✅ Add .gitignore - **НЕ ставте галочку** (у нас вже є)
   - ✅ Choose a license - **НЕ ставте галочку** (у нас вже є LICENSE)
4. Натисніть **"Create repository"**

## Крок 2: Завантаження файлів на GitHub

### Варіант А: Через веб-інтерфейс GitHub (простіше)

1. На сторінці вашого нового репозиторію натисніть **"uploading an existing file"**
2. Перетягніть всі файли з папки `C:\OpenCode\monobank\` в браузер
3. Напишіть commit message: `Initial commit - Monobank integration v1.0.0`
4. Натисніть **"Commit changes"**

### Варіант Б: Через Git (якщо встановлено)

Відкрийте термінал в папці `C:\OpenCode\monobank\` та виконайте:

```bash
# Ініціалізація git репозиторію
git init

# Додати всі файли
git add .

# Створити перший commit
git commit -m "Initial commit - Monobank integration v1.0.0"

# Додати remote репозиторій (замініть YOUR_USERNAME на ваш GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/monobank-homeassistant.git

# Перейменувати гілку на main (якщо потрібно)
git branch -M main

# Завантажити на GitHub
git push -u origin main
```

## Крок 3: Створення релізу (Release)

1. На GitHub перейдіть в розділ **"Releases"** → **"Create a new release"**
2. Заповніть форму:
   - **Tag version:** `v1.0.0`
   - **Release title:** `v1.0.0 - Initial Release`
   - **Description:** 
     ```
     ## Initial Release
     
     ### Features
     - 💳 Account balance sensors
     - 🏦 Jar (savings goals) sensors
     - 💱 Currency rate sensors (USD, EUR, GBP)
     - 🌐 Ukrainian and English localization
     - ⚙️ UI configuration flow
     ```
3. Натисніть **"Publish release"**

## Крок 4: Встановлення в Home Assistant через HACS

### Метод 1: Додати як кастомний репозиторій в HACS

1. Відкрийте **HACS** в Home Assistant
2. Натисніть на **три крапки** (⋮) в правому верхньому куті
3. Виберіть **"Custom repositories"**
4. Додайте:
   - **Repository:** `https://github.com/YOUR_USERNAME/monobank-homeassistant`
   - **Category:** `Integration`
5. Натисніть **"Add"**
6. Знайдіть **"Monobank"** в списку інтеграцій HACS
7. Натисніть **"Download"**
8. Перезапустіть Home Assistant

### Метод 2: Ручне встановлення

1. Завантажте репозиторій як ZIP з GitHub
2. Розпакуйте архів
3. Скопіюйте папку `custom_components/monobank` в папку `config/custom_components/` вашого Home Assistant
4. Структура повинна бути: `config/custom_components/monobank/`
5. Перезапустіть Home Assistant

## Крок 5: Налаштування інтеграції

1. Отримайте API токен на https://api.monobank.ua/
2. В Home Assistant перейдіть: **Settings** → **Devices & Services**
3. Натисніть **"+ Add Integration"**
4. Знайдіть **"Monobank"**
5. Введіть ваш API токен
6. Натисніть **"Submit"**

## Крок 6: Перевірка роботи

Після налаштування ви побачите нові сенсори:
- `sensor.monobank_black_xxxx` - баланси рахунків
- `sensor.monobank_jar_xxxx` - баланси банок
- `sensor.monobank_usd_uah` - курси валют

## Оновлення інтеграції

### Через HACS:
1. HACS → Integrations → Monobank
2. Натисніть **"Update"**
3. Перезапустіть Home Assistant

### Вручну:
1. Завантажте нову версію з GitHub
2. Замініть файли в `config/custom_components/monobank/`
3. Перезапустіть Home Assistant

## Підтримка

Якщо виникли проблеми:
1. Перевірте логи Home Assistant: **Settings** → **System** → **Logs**
2. Створіть issue на GitHub: https://github.com/YOUR_USERNAME/monobank-homeassistant/issues

## Корисні посилання

- 📖 Документація: README.md в репозиторії
- 🐛 Повідомити про баг: GitHub Issues
- 💡 Запропонувати функцію: GitHub Issues
- 🔑 Отримати API токен: https://api.monobank.ua/
