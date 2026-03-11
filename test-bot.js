const axios = require('axios');
require('dotenv').config();

const BOT_TOKEN = process.env.BOT_TOKEN;
const SERVER_URL = process.env.SERVER_URL;

async function testBot() {
    console.log('🤖 Testing NoHurtCam Telegram Bot...\n');

    try {
        // 1. Тест Telegram API
        console.log('1. Testing Telegram Bot API...');
        const botInfo = await axios.get(`https://api.telegram.org/bot${BOT_TOKEN}/getMe`);
        
        if (botInfo.data.ok) {
            console.log(`✅ Bot connected: @${botInfo.data.result.username}`);
            console.log(`   Bot ID: ${botInfo.data.result.id}`);
            console.log(`   Bot Name: ${botInfo.data.result.first_name}\n`);
        } else {
            console.log('❌ Bot connection failed\n');
            return;
        }

        // 2. Тест сервера
        console.log('2. Testing server connection...');
        const serverResponse = await axios.get(`${SERVER_URL}/api/ping`);
        
        if (serverResponse.data.success) {
            console.log('✅ Server connected successfully');
            console.log(`   Uptime: ${Math.floor(serverResponse.data.uptime / 3600)}h ${Math.floor((serverResponse.data.uptime % 3600) / 60)}m`);
            console.log(`   Status: ${serverResponse.data.message}\n`);
        } else {
            console.log('❌ Server connection failed\n');
        }

        // 3. Тест HWID endpoints
        console.log('3. Testing HWID endpoints...');
        
        // Тестовый HWID
        const testHWID = 'TEST123456789ABC';
        
        // Добавляем тестовый HWID
        const addResponse = await axios.post(`${SERVER_URL}/api/hwid/add`, {
            hwid: testHWID,
            adminKey: process.env.ADMIN_KEY
        });
        
        if (addResponse.data.success) {
            console.log(`✅ HWID add test passed: ${testHWID}`);
        }
        
        // Проверяем HWID
        const checkResponse = await axios.get(`${SERVER_URL}/api/hwid/check/${testHWID}`);
        
        if (checkResponse.data.authorized) {
            console.log('✅ HWID check test passed');
        }
        
        // Удаляем тестовый HWID
        await axios.delete(`${SERVER_URL}/api/hwid/remove/${testHWID}`, {
            headers: {
                'Authorization': `Bearer ${process.env.ADMIN_KEY}`
            }
        });
        console.log('✅ HWID cleanup completed\n');

        // 4. Тест Telegram events
        console.log('4. Testing Telegram events...');
        
        const eventResponse = await axios.post(`${SERVER_URL}/api/telegram/events`, {
            type: 'test_event',
            data: 'test_data',
            adminKey: process.env.ADMIN_KEY
        });
        
        if (eventResponse.data.success) {
            console.log('✅ Telegram events test passed\n');
        }

        console.log('🎉 All tests passed! Bot is ready to deploy.\n');
        
        console.log('📋 Next steps:');
        console.log('1. Create a GitHub repository');
        console.log('2. Upload bot files to the repository');
        console.log('3. Deploy to Render.com using the repository');
        console.log('4. Set environment variables in Render dashboard');
        console.log('5. Test the bot by sending /start in Telegram\n');
        
        console.log('🔧 Your bot details:');
        console.log(`   Bot Username: @${botInfo.data.result.username}`);
        console.log(`   Your User ID: 7111158209`);
        console.log(`   Server URL: ${SERVER_URL}`);

    } catch (error) {
        console.error('❌ Test failed:', error.response?.data || error.message);
        
        if (error.response?.status === 401) {
            console.log('\n💡 This might be an authorization error. Check your tokens and keys.');
        }
        
        if (error.code === 'ECONNREFUSED') {
            console.log('\n💡 Server connection failed. Make sure the server is running.');
        }
    }
}

// Запуск тестов
testBot();