import aiohttp
import asyncio
from typing import Dict, List, Optional, Tuple
from config import FUNTIME_EVENTS_API

EVENT_INFO = {
    "myst_beacon": {
        "name": "Загадочный маяк",
        "icon": "🗼",
        "desc": "Загадочный маяк искажает пространство. Активируй его и забери редкую награду!"
    },
    "mystic": {
        "name": "Мистический сундук",
        "icon": "💎",
        "desc": "Мистический сундук с ценными артефактами и ресурсами."
    },
    "beacon": {
        "name": "Маяк убийца",
        "icon": "🚨",
        "desc": "Маяк смерти притягивает сильнейших игроков сервера."
    },
    "airdrop": {
        "name": "Аирдроп",
        "icon": "📦",
        "desc": "Сброшенный с неба сундук с ценными ресурсами и снаряжением."
    },
    "vulkan": {
        "name": "Вулкан",
        "icon": "🌋",
        "desc": "Извержение вулкана с выбросом редчайших сокровищ."
    },
    "geyser": {
        "name": "Гейзер",
        "icon": "💨",
        "desc": "Мощный гейзер, выталкивающий ресурсы на поверхность."
    },
    "altarundead": {
        "name": "Алтарь нежити",
        "icon": "⚡",
        "desc": "Древний алтарь, охраняемый волнами опасных мобов."
    },
    "meteor_rain": {
        "name": "Метеоритный дождь",
        "icon": "☄️",
        "desc": "Падение метеоритов с космической рудой и лутом."
    },
    "deathchest": {
        "name": "Сундук смерти",
        "icon": "☠️",
        "desc": "Опасный сундук посреди смертельной зоны."
    },
    "hellm": {
        "name": "Адский маяк",
        "icon": "🔥",
        "desc": "Адское пламя и ценный дроп из Нижнего мира."
    },
    "vote": {
        "name": "Голосование",
        "icon": "🗳",
        "desc": "Игровое голосование за следующий ивент."
    }
}

PHASE_INFO = {
    "WAITING": ("⏳", "Появление", "Ожидание спавна на сервере"),
    "STARTING": ("⏳", "Готовится", "Скоро появятся координаты"),
    "ACTIVATING": ("⚡", "Активация", "Скоро начнет выдавать лут"),
    "RUNNING": ("⚔️", "Идет бой", "Ивент активен"),
    "OPENED": ("🎁", "Открыт", "Сундук открыт - забирай лут"),
    "LOOTING": ("🎁", "Лут готов", "Беги забирать лут!"),
    "FINISHED": ("🏁", "Завершен", "Ивент окончен"),
    "CLOSED": ("🏁", "Завершен", "Ивент окончен"),
    "VOTING": ("🗳", "Голосование", "Идет выбор ивента")
}

def format_time_left(seconds: int) -> str:
    """Formats seconds into readable MM:SS or HH:MM:SS."""
    if seconds <= 0:
        return "0:00"
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    if h > 0:
        return f"{h} ч {m:02d} мин"
    if m > 0:
        return f"{m} мин {s:02d} сек"
    return f"{s} сек"

def format_server_name(raw_server: str) -> Tuple[str, str]:
    """Returns (display_name, join_command), e.g. ('Анархия 104', '/anarchy104')."""
    raw = str(raw_server).strip().lower()
    if raw.startswith("anarchy"):
        num = raw.replace("anarchy", "")
        return f"Анархия {num}", f"/anarchy{num}"
    return raw.capitalize(), f"/{raw}"

async def fetch_funtime_events() -> List[Dict]:
    """
    Fetches raw events from FunTime API and returns normalized event items.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Referer": "https://funtime.me/events"
    }
    
    timeout = aiohttp.ClientTimeout(total=8)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(FUNTIME_EVENTS_API, headers=headers) as resp:
            if resp.status != 200:
                raise Exception(f"FunTime API returned HTTP status {resp.status}")
            data = await resp.json()
            
    servers = data.get("response", [])
    parsed_events = []
    
    for srv in servers:
        server_raw = srv.get("server", "")
        server_name, join_cmd = format_server_name(server_raw)
        
        for ev in srv.get("events", []):
            ev_type = ev.get("event-type", "")
            if ev_type == "system":
                # Skip pure system timer if no actual event ID
                continue
                
            ev_id = ev.get("id", "unknown")
            info = EVENT_INFO.get(ev_id, {
                "name": ev_id.replace("_", " ").title(),
                "icon": "✨",
                "desc": "Специальное игровое событие FunTime"
            })
            
            phase_raw = ev.get("phase", "RUNNING").upper()
            phase_icon, phase_name, phase_desc = PHASE_INFO.get(
                phase_raw, ("🔹", phase_raw, "Активно")
            )
            
            # Prefer time-seconds-left, then calculate from time-ms-left
            time_left_sec = ev.get("time-seconds-left")
            if time_left_sec is None:
                ms = ev.get("time-ms-left")
                time_left_sec = int(ms / 1000) if ms is not None else 0
            else:
                time_left_sec = int(time_left_sec)
                
            time_str = format_time_left(time_left_sec)
            
            loc_announced = ev.get("location-announced", False)
            loc_data = ev.get("location-event")
            coords_str = None
            if loc_announced and loc_data:
                x = loc_data.get("x")
                y = loc_data.get("y")
                z = loc_data.get("z")
                if x is not None and z is not None:
                    coords_str = f"X: {x}, Y: {y}, Z: {z}" if y is not None else f"X: {x}, Z: {z}"
            
            parsed_events.append({
                "id": ev_id,
                "name": info["name"],
                "icon": info["icon"],
                "desc": info["desc"],
                "server_raw": server_raw,
                "server_name": server_name,
                "join_cmd": join_cmd,
                "phase_raw": phase_raw,
                "phase_icon": phase_icon,
                "phase_name": phase_name,
                "phase_desc": phase_desc,
                "time_sec": time_left_sec,
                "time_str": time_str,
                "coords": coords_str,
                "location_announced": loc_announced,
                "loot": ev.get("loot")
            })
            
    # Sort events:
    # 1. ACTIVATING with positive time (imminent loot)
    # 2. RUNNING with positive time (active battle)
    # 3. STARTING / WAITING (upcoming)
    # 4. LOOTING / OPENED (already dropped)
    # 5. CLOSED / FINISHED
    def sort_key(item):
        phase = item["phase_raw"]
        time_sec = item["time_sec"]
        
        if phase == "ACTIVATING":
            return (0, time_sec)
        elif phase == "RUNNING":
            return (1, time_sec if time_sec > 0 else 9999)
        elif phase in ["STARTING", "WAITING", "VOTING"]:
            return (2, time_sec if time_sec > 0 else 9999)
        elif phase in ["LOOTING", "OPENED"]:
            return (3, 0)
        else:
            return (4, time_sec)
        
    parsed_events.sort(key=sort_key)
    return parsed_events
