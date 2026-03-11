# Деплой Telegram бота на Render.com

## 🚀 Быстрый деплой (рекомендуется)

### Шаг 1: Подготовка GitHub репозитория
1. Создайте новый репозиторий на GitHub
2. Загрузите папку `telegram-bot/` в корень репозитория
3. Структура должна быть:
   ```
   your-repo/
   ├── bot.js
   ├── package.json
   ├── .env
   ├── render.yaml
   └── DEPLOY.md
   ```

### Шаг 2: Деплой на Render.com
1. Зайдите на https://render.com
2. Нажмите "New +" → "Web Service"
3. Подключите ваш GitHub репозиторий
4. Настройки:
   - **Name**: `nohurtcam-telegram-bot`
   - **Environment**: `Node`
   - **Build Command**: `npm install`
   - **Start Command**: `npm start`
   - **Instance Type**: `Free` (достаточно для бота)

### Шаг 3: Переменные окружения
В разделе "Environment Variables" добавьте:
- `BOT_TOKEN` = `8664085358:AAFBrWTBnhvA_VzpukG5-Cz9sdTn3cV6ynA`
- `SERVER_URL` = `https://serverml-wv0z.onrender.com`
- `ADMIN_KEY` = `admin-secret-key-2024`
- `NODE_ENV` = `production`

### Шаг 4: Деплой
1. Нажмите "Create Web Service"
2. Дождитесь завершения деплоя (2-3 минуты)
3. Бот автоматически запустится и будет работать 24/7

## 🔧 Альтернативные варианты деплоя

### Heroku
1. Установите Heroku CLI
2. В папке `telegram-bot/`:
   ```bash
   heroku create nohurtcam-bot
   heroku config:set BOT_TOKEN=8664085358:AAFBrWTBnhvA_VzpukG5-Cz9sdTn3cV6ynA
   heroku config:set SERVER_URL=https://serverml-wv0z.onrender.com
   heroku config:set ADMIN_KEY=admin-secret-key-2024
   git push heroku main
   ```

### Railway
1. Зайдите на https://railway.app
2. Подключите GitHub репозиторий
3. Добавьте переменные окружения
4. Деплой произойдет автоматически

### VPS (Ubuntu/Debian)
```bash
# Установка Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Клонирование и запуск
git clone your-repo
cd telegram-bot
npm install
npm install -g pm2

# Запуск с PM2 (автоперезапуск)
pm2 start bot.js --name "nohurtcam-bot"
pm2 startup
pm2 save
```

## ✅ Проверка работы

После деплоя:
1. Найдите вашего бота в Telegram: @your_bot_username
2. Отправьте `/start`
3. Должно появиться приветственное сообщение
4. Попробуйте команду `/help`

## 📊 Мониторинг

### Render.com:
- Логи доступны в панели управления
- Автоматический перезапуск при сбоях
- Метрики использования ресурсов

### Команды для проверки:
- `/stats` - статистика сервера
- Логи бота покажут все операции

## 🔄 Обновление бота

1. Внесите изменения в код
2. Сделайте commit и push в GitHub
3. Render автоматически переразвернет бота
4. Или нажмите "Manual Deploy" в панели Render

## 🛠️ Troubleshooting

### Бот не отвечает:
1. Проверьте логи в Render панели
2. Убедитесь что токен правильный
3. Проверьте переменные окружения

### Ошибки авторизации:
1. Проверьте что ваш User ID (7111158209) в списке ADMIN_IDS
2. Убедитесь что ADMIN_KEY совпадает с сервером

### Проблемы с сервером:
1. Проверьте что SERVER_URL доступен
2. Попробуйте команду `/stats` для проверки связи

## 📁 Файлы для загрузки

Загрузите эти файлы в корень GitHub репозитория:
- `bot.js` - основной код бота
- `package.json` - зависимости
- `.env` - переменные окружения (уже настроен)
- `render.yaml` - конфигурация для Render (опционально)
- `DEPLOY.md` - эта инструкция

**Важно**: Не загружайте `.env` файл в публичный репозиторий! Используйте переменные окружения в Render панели.