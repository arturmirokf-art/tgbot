const TelegramBot = require('node-telegram-bot-api');
const axios = require('axios');
const express = require('express');
require('dotenv').config();

// Express сервер для Render.com (требует открытый порт)
const app = express();
const PORT = process.env.PORT || 3000;

app.get('/', (req, res) => {
    res.json({
        status: 'NoHurtCam Telegram Bot is running',
        uptime: process.uptime(),
        timestamp: new Date().toISOString()
    });
});

app.get('/health', (req, res) => {
    res.json({ status: 'healthy', bot: 'running' });
});

app.listen(PORT, () => {
    console.log(`HTTP server running on port ${PORT}`);
});

// Замените на ваш токен бота от @BotFather
const BOT_TOKEN = process.env.BOT_TOKEN || '8664085358:AAFBrWTBnhvA_VzpukG5-Cz9sdTn3cV6ynA';
const SERVER_URL = process.env.SERVER_URL || 'https://serverml-wv0z.onrender.com';
const ADMIN_KEY = process.env.ADMIN_KEY || 'admin-secret-key-2024';

// Список админов (Telegram User ID)
const ADMIN_IDS = [
    7111158209, // Ваш Telegram User ID
    // Добавьте другие админские ID если нужно
];

const bot = new TelegramBot(BOT_TOKEN, { polling: true });

console.log('NoHurtCam Telegram Bot started!');

// Проверка админских прав
function isAdmin(userId) {
    return ADMIN_IDS.includes(userId);
}

// Команда /start
bot.onText(/\/start/, (msg) => {
    const chatId = msg.chat.id;
    const userId = msg.from.id;
    
    if (!isAdmin(userId)) {
        bot.sendMessage(chatId, '❌ Access denied. This bot is for authorized admins only.');
        return;
    }
    
    const welcomeMessage = `
🎮 NoHurtCam Admin Bot

Available commands:
/hwid_add <HWID> - Add HWID to whitelist
/hwid_remove <HWID> - Remove HWID from whitelist  
/hwid_list - Show all authorized HWIDs
/play_music - Play RAKAI music for all users
/stop_music - Stop RAKAI music
/stats - Show server statistics
/help - Show this help message

Your User ID: ${userId}
`;
    
    bot.sendMessage(chatId, welcomeMessage);
});

// Команда /help
bot.onText(/\/help/, (msg) => {
    const chatId = msg.chat.id;
    const userId = msg.from.id;
    
    if (!isAdmin(userId)) {
        bot.sendMessage(chatId, '❌ Access denied.');
        return;
    }
    
    const helpMessage = `
📋 NoHurtCam Admin Commands

HWID Management:
/hwid_add ABC123DEF456 - Add HWID to authorized list
/hwid_remove ABC123DEF456 - Remove HWID from list
/hwid_list - Show all authorized HWIDs

Music Control:
/play_music - Play RAKAI music for all mod users
/stop_music - Stop RAKAI music overlay

Information:
/stats - Server and user statistics
/help - Show this help

How to get HWID:
1. Run the mod once
2. Check console output for "NoHurtCam HWID: XXXXXXXX"
3. Use /hwid_add command to authorize it
`;
    
    bot.sendMessage(chatId, helpMessage);
});

// Команда добавления HWID
bot.onText(/\/hwid_add (.+)/, async (msg, match) => {
    const chatId = msg.chat.id;
    const userId = msg.from.id;
    const hwid = match[1].trim().toUpperCase();
    
    if (!isAdmin(userId)) {
        bot.sendMessage(chatId, '❌ Access denied.');
        return;
    }
    
    if (hwid.length < 8) {
        bot.sendMessage(chatId, '❌ Invalid HWID format. HWID should be at least 8 characters.');
        return;
    }
    
    try {
        const response = await axios.post(`${SERVER_URL}/api/hwid/add`, {
            hwid: hwid,
            adminKey: ADMIN_KEY
        });
        
        if (response.data.success) {
            bot.sendMessage(chatId, `✅ HWID added successfully!\n\n🔑 HWID: ${hwid}\n👥 Total authorized: ${response.data.totalAuthorized}`);
        } else {
            bot.sendMessage(chatId, `❌ Failed to add HWID: ${response.data.error}`);
        }
    } catch (error) {
        console.error('HWID add error:', error.message);
        bot.sendMessage(chatId, '❌ Server error. Please try again later.');
    }
});

// Команда удаления HWID
bot.onText(/\/hwid_remove (.+)/, async (msg, match) => {
    const chatId = msg.chat.id;
    const userId = msg.from.id;
    const hwid = match[1].trim().toUpperCase();
    
    if (!isAdmin(userId)) {
        bot.sendMessage(chatId, '❌ Access denied.');
        return;
    }
    
    try {
        const response = await axios.delete(`${SERVER_URL}/api/hwid/remove/${hwid}`, {
            headers: {
                'Authorization': `Bearer ${ADMIN_KEY}`
            }
        });
        
        if (response.data.success) {
            bot.sendMessage(chatId, `✅ HWID removed successfully!\n\n🔑 HWID: ${hwid}\n👥 Total authorized: ${response.data.totalAuthorized}`);
        } else {
            bot.sendMessage(chatId, `❌ ${response.data.message}`);
        }
    } catch (error) {
        console.error('HWID remove error:', error.message);
        bot.sendMessage(chatId, '❌ Server error. Please try again later.');
    }
});

// Команда списка HWID
bot.onText(/\/hwid_list/, async (msg) => {
    const chatId = msg.chat.id;
    const userId = msg.from.id;
    
    if (!isAdmin(userId)) {
        bot.sendMessage(chatId, '❌ Access denied.');
        return;
    }
    
    try {
        const response = await axios.get(`${SERVER_URL}/api/hwid/list`, {
            headers: {
                'Authorization': `Bearer ${ADMIN_KEY}`
            }
        });
        
        const hwids = response.data;
        
        if (hwids.length === 0) {
            bot.sendMessage(chatId, '📝 No authorized HWIDs found.');
            return;
        }
        
        let message = `📝 Authorized HWIDs (${hwids.length}):\n\n`;
        hwids.forEach((hwid, index) => {
            message += `${index + 1}. ${hwid}\n`;
        });
        
        bot.sendMessage(chatId, message);
    } catch (error) {
        console.error('HWID list error:', error.message);
        bot.sendMessage(chatId, '❌ Server error. Please try again later.');
    }
});

// Команда воспроизведения музыки
bot.onText(/\/play_music/, async (msg) => {
    const chatId = msg.chat.id;
    const userId = msg.from.id;
    
    if (!isAdmin(userId)) {
        bot.sendMessage(chatId, '❌ Access denied.');
        return;
    }
    
    try {
        const response = await axios.post(`${SERVER_URL}/api/telegram/events`, {
            type: 'play_music',
            data: 'rakai_music',
            adminKey: ADMIN_KEY
        });
        
        if (response.data.success) {
            bot.sendMessage(chatId, '🎵 RAKAI music started for all users!\n\n🎮 All mod users will now see the RAKAI overlay and hear the music.');
        } else {
            bot.sendMessage(chatId, `❌ Failed to start music: ${response.data.error}`);
        }
    } catch (error) {
        console.error('Play music error:', error.message);
        bot.sendMessage(chatId, '❌ Server error. Please try again later.');
    }
});

// Команда остановки музыки
bot.onText(/\/stop_music/, async (msg) => {
    const chatId = msg.chat.id;
    const userId = msg.from.id;
    
    if (!isAdmin(userId)) {
        bot.sendMessage(chatId, '❌ Access denied.');
        return;
    }
    
    try {
        const response = await axios.post(`${SERVER_URL}/api/telegram/events`, {
            type: 'stop_music',
            data: '',
            adminKey: ADMIN_KEY
        });
        
        if (response.data.success) {
            bot.sendMessage(chatId, '🔇 RAKAI music stopped for all users.');
        } else {
            bot.sendMessage(chatId, `❌ Failed to stop music: ${response.data.error}`);
        }
    } catch (error) {
        console.error('Stop music error:', error.message);
        bot.sendMessage(chatId, '❌ Server error. Please try again later.');
    }
});

// Команда статистики
bot.onText(/\/stats/, async (msg) => {
    const chatId = msg.chat.id;
    const userId = msg.from.id;
    
    if (!isAdmin(userId)) {
        bot.sendMessage(chatId, '❌ Access denied.');
        return;
    }
    
    try {
        const response = await axios.get(`${SERVER_URL}/api/ping`);
        const stats = response.data.stats;
        
        const statsMessage = `
📊 Server Statistics

🕐 Uptime: ${Math.floor(stats.uptime / 3600)}h ${Math.floor((stats.uptime % 3600) / 60)}m
👥 Authorized Users: ${stats.authorizedUsers || 0}
📁 Total Configs: ${stats.totalConfigs || 0}
📈 ML Samples: ${stats.totalSamples || 0}
📤 Uploads: ${stats.totalUploads || 0}
📥 Downloads: ${stats.totalDownloads || 0}

🌐 Server: Online ✅
`;
        
        bot.sendMessage(chatId, statsMessage);
    } catch (error) {
        console.error('Stats error:', error.message);
        bot.sendMessage(chatId, '❌ Server error. Please try again later.');
    }
});

// Обработка неизвестных команд
bot.on('message', (msg) => {
    const chatId = msg.chat.id;
    const userId = msg.from.id;
    const text = msg.text;
    
    // Игнорируем команды, которые уже обработаны
    if (text && text.startsWith('/') && !text.match(/\/(start|help|hwid_add|hwid_remove|hwid_list|play_music|stop_music|stats)/)) {
        if (!isAdmin(userId)) {
            bot.sendMessage(chatId, '❌ Access denied.');
            return;
        }
        
        bot.sendMessage(chatId, '❓ Unknown command. Use /help to see available commands.');
    }
});

// Обработка ошибок
bot.on('error', (error) => {
    console.error('Bot error:', error);
});

bot.on('polling_error', (error) => {
    console.error('Polling error:', error);
});

console.log('Bot is running. Send /start to begin.');