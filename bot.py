import asyncio
import logging
import os
import sys
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import BOT_TOKEN, PORT, HOST
from handlers import start, events, seed_search
from services.seed_db import init_csv, load_all_seeds, save_seed, sync_mod_csv

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("FunTimeBot")

# Initialize aiohttp Web Application for Render.com & UptimeRobot
async def health_check(request):
    return web.json_response({
        "status": "ok",
        "service": "FunTime Telegram Bot",
        "bot": "@Ovosh1337bot",
        "healthy": True
    })

async def get_seeds_api(request):
    sync_mod_csv()
    seeds = load_all_seeds()
    return web.json_response({
        "status": "ok",
        "total_anarchies": len(seeds),
        "seeds": {k: {"seed": v[0], "updated_at": v[1]} for k, v in seeds.items()}
    })

async def add_seed_api(request):
    try:
        data = await request.json()
        anarchy = str(data.get("anarchy", "")).strip()
        seed = str(data.get("seed", "")).strip()
        updated_at = str(data.get("updated_at", "")).strip()
        if not anarchy or not seed:
            return web.json_response({"status": "error", "message": "anarchy and seed required"}, status=400)
        success = save_seed(anarchy, seed, updated_at)
        return web.json_response({"status": "ok" if success else "error"})
    except Exception as e:
        return web.json_response({"status": "error", "message": str(e)}, status=500)

def create_web_app() -> web.Application:
    app = web.Application()
    app.router.add_get("/", health_check)
    app.router.add_get("/health", health_check)
    app.router.add_get("/api/seeds", get_seeds_api)
    app.router.add_post("/api/seed", add_seed_api)
    return app

async def main():
    logger.info("Initializing FunTime Bot...")
    init_csv()
    sync_mod_csv()
    
    # Create Bot and Dispatcher
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()
    
    # Include handler routers
    dp.include_router(start.router)
    dp.include_router(events.router)
    dp.include_router(seed_search.router)
    
    # Create Web Runner for Render health checks & UptimeRobot
    web_app = create_web_app()
    runner = web.AppRunner(web_app)
    await runner.setup()
    site = web.TCPSite(runner, HOST, PORT)
    await site.start()
    logger.info(f"Web server started on http://{HOST}:{PORT} for UptimeRobot health check")

    # Start Bot Polling
    try:
        # Delete webhook if any was set before
        await bot.delete_webhook(drop_pending_updates=True)
        logger.info("Starting Telegram bot polling...")
        await dp.start_polling(bot)
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopping...")
    finally:
        await bot.session.close()
        await runner.cleanup()
        logger.info("Shutdown completed.")

if __name__ == "__main__":
    asyncio.run(main())
