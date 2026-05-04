# Швидкий старт: Завантаження на GitHub

## Покрокова інструкція

### 📋 Що потрібно зробити:

1. ✅ Створити репозиторій на GitHub
2. ✅ Завантажити файли
3. ✅ Встановити в Home Assistant

---

## 1️⃣ Створення репозиторію на GitHub

### Крок 1: Створіть новий репозиторій
1. Перейдіть на https://github.com/new
2. Заповніть:
   - **Repository name:** `monobank-homeassistant`
   - **Description:** `Monobank integration for Home Assistant`
   - Виберіть **Public**
   - **НЕ** ставте галочки на README, .gitignore, License
3. Натисніть **"Create repository"**

---

## 2️⃣ Завантаження файлів (НАЙПРОСТІШИЙ СПОСІБ)

### Через веб-інтерфейс GitHub:

1. На сторінці нового репозиторію знайдіть текст **"uploading an existing file"** і натисніть на нього
   
2. Відкрийте провідник Windows і перейдіть в папку:
   ```
   C:\OpenCode\monobank\
   ```

3. Виберіть ВСІ файли та папки (Ctrl+A), КРІМ:
   - `Новий Текстовий документ (2).txt` (це тестовий файл)

4. Перетягніть файли в вікно браузера GitHub

5. В полі "Commit changes" напишіть:
   ```
   Initial commit - Monobank integration v1.0.0
   ```

6. Натисніть **"Commit changes"**

✅ Готово! Ваш код тепер на GitHub!

---

## 3️⃣ Створення релізу (Release)

1. На GitHub перейдіть на вкладку **"Releases"** (праворуч)
2. Натисніть **"Create a new release"**
3. Заповніть:
   - **Choose a tag:** напишіть `v1.0.0` і натисніть "Create new tag"
   - **Release title:** `v1.0.0 - Initial Release`
   - **Description:**
     ```markdown
     ## 🎉 Initial Release
     
     Перша версія інтеграції Monobank для Home Assistant!
     
     ### ✨ Функціонал
     - 💳 Сенсори балансів рахунків (всі типи карток)
     - 🏦 Сенсори банок (цілей накопичення)
     - 💱 Курси валют (USD, EUR, GBP)
     - 🌐 Українська та англійська локалізація
     - ⚙️ Конфігурація через UI
     
     ### 📦 Встановлення
     Дивіться [INSTALLATION.md](INSTALLATION.md)
     
     ### 🔑 API токен
     Отримайте на https://api.monobank.ua/
     ```
4. Натисніть **"Publish release"**

---

## 4️⃣ Встановлення в Home Assistant

### Варіант А: Через HACS (рекомендовано)

1. Відкрийте **HACS** в Home Assistant
2. Натисніть **⋮** (три крапки) → **Custom repositories**
3. Додайте:
   - **Repository:** `https://github.com/ВАШ_USERNAME/monobank-homeassistant`
   - **Category:** `Integration`
4. Натисніть **"Add"**
5. Закрийте вікно
6. Знайдіть **"Monobank"** в списку
7. Натисніть **"Download"**
8. **Перезапустіть Home Assistant**

### Варіант Б: Ручне встановлення

1. Завантажте ZIP з GitHub:
   - На сторінці репозиторію натисніть **Code** → **Download ZIP**

2. Розпакуйте архів

3. Скопіюйте папку `custom_components/monobank` в:
   ```
   /config/custom_components/monobank/
   ```
   (створіть папку `custom_components` якщо її немає)

4. **Перезапустіть Home Assistant**

---

## 5️⃣ Налаштування інтеграції

1. **Отримайте API токен:**
   - Перейдіть на https://api.monobank.ua/
   - Увійдіть через Monobank
   - Скопіюйте токен

2. **Додайте інтеграцію:**
   - Settings → Devices & Services
   - Натисніть **+ Add Integration**
   - Знайдіть **"Monobank"**
   - Вставте API токен
   - Натисніть **Submit**

3. **Перевірте сенсори:**
   - Developer Tools → States
   - Знайдіть сенсори `sensor.monobank_*`

---

## 🎯 Готово!

Тепер у вас є:
- ✅ Репозиторій на GitHub
- ✅ Інтеграція в Home Assistant
- ✅ Сенсори балансів та курсів валют

### Що далі?

- 📊 Створіть Lovelace картки для відображення балансів
- 🔔 Налаштуйте автоматизації (наприклад, сповіщення при низькому балансі)
- 🌟 Поставте зірку репозиторію на GitHub
- 🐛 Повідомте про баги через GitHub Issues

---

## 📝 Корисні посилання

- 📖 Повна документація: [README.md](README.md)
- 🔧 Детальна інструкція: [INSTALLATION.md](INSTALLATION.md)
- 📋 План розробки: [INTEGRATION_PLAN.md](INTEGRATION_PLAN.md)
- 🔑 API токен: https://api.monobank.ua/
- 💬 GitHub Issues: `https://github.com/ВАШ_USERNAME/monobank-homeassistant/issues`

---

## ❓ Проблеми?

### Інтеграція не з'являється в списку
- Перевірте, що папка `custom_components/monobank` існує
- Перезапустіть Home Assistant
- Перевірте логи: Settings → System → Logs

### Помилка "Invalid API token"
- Перевірте токен на https://api.monobank.ua/
- Переконайтесь, що токен скопійовано повністю

### Сенсори не оновлюються
- Перевірте інтернет з'єднання
- Monobank API має ліміт 60 запитів/хвилину
- Перевірте логи Home Assistant

---

**Успіхів! 🚀**
