# 🚀 Инструкция по развертыванию на Render.com + UptimeRobot (Бесплатно 24/7)

## 📌 О боте
- **Имя бота:** `@Ovosh1337bot`
- **Функции:**
  1. 📦 Парсинг и интерактивная пагинация ивентов с `funtime.me` (по 10 ивентов на страницу с таймерами и координатами).
  2. 🔍 Поиск похожих анархий по общей сид-генерации мира.
  3. 🌐 Встроенный HTTP-сервер для health check мониторинга UptimeRobot.

---

## 🛠 Шаг 1: Загрузка бота на GitHub
1. Создайте новый репозиторий на [GitHub.com](https://github.com/new) (например: `funtime-tg-bot`).
2. В папке `telegram_bot` инициализируйте git и загрузите файлы:
```bash
cd telegram_bot
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/ВАШ_НИК/funtime-tg-bot.git
git push -u origin main
```

---

## ☁️ Шаг 2: Развертывание на Render.com (Free Plan)
1. Зарегистрируйтесь / войдите на [render.com](https://dashboard.render.com/).
2. Нажмите **New +** -> **Web Service**.
3. Подключите ваш GitHub репозиторий `funtime-tg-bot`.
4. Заполните параметры конфигурации:
   - **Name:** `funtime-helper-bot` (или любое имя)
   - **Region:** `Frankfurt (EU Central)` или любой ближайший
   - **Branch:** `main`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python bot.py`
   - **Instance Type:** `Free`
5. В разделе **Environment Variables** (переменные окружения) добавьте:
   - `BOT_TOKEN` = `8751158476:AAF32VXefnx8ZfEgjaKB_Ps1l-9iA9ZWO1U`
   - `PORT` = `10000`
6. Нажмите **Deploy Web Service**.
7. Дождитесь статуса **Live** и скопируйте предоставленный URL (например: `https://funtime-helper-bot.onrender.com`).

---

## ⏱ Шаг 3: Настройка UptimeRobot (24/7 без ухода в сон)
Бесплатные сервисы Render засыпают через 15 минут неактивности, если на них нет входящих HTTP-запросов. В бот встроен веб-сервер, который отдает `200 OK` на любые запросы к `/health`.

1. Зарегистрируйтесь на [uptimerobot.com](https://uptimerobot.com/).
2. Нажмите **+ Add New Monitor**.
3. Заполните настройки:
   - **Monitor Type:** `HTTP(s)`
   - **Friendly Name:** `FunTime Bot`
   - **URL (or IP):** `https://funtime-helper-bot.onrender.com/health` (ваш URL от Render)
   - **Monitoring Interval:** `Every 5 minutes` (Каждые 5 минут)
4. Нажмите **Create Monitor**.

🎉 **Готово!** Теперь UptimeRobot будет опрашивать веб-сервер каждые 5 минут, и бот в Telegram будет работать непрерывно 24/7!
