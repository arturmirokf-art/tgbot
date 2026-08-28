# 🚀 Развертывание бота на Render.com (Ваш сервис: https://tgbot-1-jngl.onrender.com)

## 📌 Данные вашего проекта
- **Ссылка Render:** `https://tgbot-1-jngl.onrender.com`
- **Ссылка для UptimeRobot:** `https://tgbot-1-jngl.onrender.com/health`
- **Репозиторий GitHub:** `arturmirokf-art/tgbot`
- **Токен бота:** `8751158476:AAF32VXefnx8ZfEgjaKB_Ps1l-9iA9ZWO1U`
- **Имя бота в Telegram:** `@Ovosh1337bot`

---

## ⚙️ Настройки в панели Render.com

1. **Language / Runtime:** `Python 3`
2. **Build Command:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Start Command:**
   ```bash
   python bot.py
   ```
4. **Environment Variables:**
   - `BOT_TOKEN` = `8751158476:AAF32VXefnx8ZfEgjaKB_Ps1l-9iA9ZWO1U`
   - `PORT` = `10000`

---

## ⏱ Настройка UptimeRobot (24/7 без засыпания)
1. Откройте [uptimerobot.com](https://uptimerobot.com/).
2. Нажмите **+ Add New Monitor**.
3. Заполните:
   - **Monitor Type:** `HTTP(s)`
   - **Friendly Name:** `FunTime Telegram Bot`
   - **URL (or IP):** `https://tgbot-1-jngl.onrender.com/health`
   - **Monitoring Interval:** `Every 5 minutes`
4. Нажмите **Create Monitor**.
