import os
from pathlib import Path

# Telegram Bot Settings
BOT_TOKEN = os.getenv("BOT_TOKEN", "8751158476:AAF32VXefnx8ZfEgjaKB_Ps1l-9iA9ZWO1U")
BOT_USERNAME = os.getenv("BOT_USERNAME", "Ovosh1337bot")

# Server / Render Settings
PORT = int(os.getenv("PORT", 8080))
HOST = os.getenv("HOST", "0.0.0.0")

# Paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
CSV_PATH = DATA_DIR / "anarchy_seeds.csv"

# Fallback / mod path (local directory)
SYSTEMDLC_DIR = BASE_DIR.parent / "SystemDLC-main"
SYSTEMDLC_CSV_PATH = SYSTEMDLC_DIR / "run" / "anarchy_seeds.csv"

# FunTime API Settings
FUNTIME_EVENTS_API = "https://funtime.me/api/backend/api/v1/events"
ITEMS_PER_PAGE = 10
