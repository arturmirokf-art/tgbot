import math
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from services.funtime_api import fetch_funtime_events
from config import ITEMS_PER_PAGE

router = Router()

def build_events_page_text(events: list, page: int, total_pages: int, filter_mode: str) -> str:
    """Builds clean and styled message text for a page of events."""
    filter_names = {
        "all": "🌐 Все события",
        "active": "⚡ Активные (Идет бой / Активация / Лут)",
        "upcoming": "⏳ Готовятся / Ожидание"
    }
    
    header = (
        f"📦 <b>События на серверах FunTime</b>\n"
        f"Фильтр: <b>{filter_names.get(filter_mode, 'Все')}</b>\n"
        f"Найдено: <b>{len(events)}</b> ивентов | Страница <b>{page + 1}</b> из <b>{total_pages}</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
    )
    
    if not events:
        return (
            header +
            "<i>На данный момент по выбранному фильтру нет активных событий.</i>\n\n"
            "🔄 Нажмите «Обновить», чтобы запросить свежие данные."
        )
        
    start_idx = page * ITEMS_PER_PAGE
    page_items = events[start_idx : start_idx + ITEMS_PER_PAGE]
    
    cards = []
    for i, ev in enumerate(page_items, start=start_idx + 1):
        icon = ev["icon"]
        name = ev["name"]
        server = ev["server_name"]
        cmd = ev["join_cmd"]
        phase_icon = ev["phase_icon"]
        phase_name = ev["phase_name"]
        phase_raw = ev["phase_raw"]
        time_sec = ev["time_sec"]
        time_str = ev["time_str"]
        coords = ev["coords"]
        
        # Build status & timer line
        if phase_raw == "ACTIVATING":
            if time_sec > 0:
                status_line = f"⚡ <b>Активация</b> • ⏱ <code>{time_str}</code> (до лута)"
            else:
                status_line = f"⚡ <b>Активация</b> • ⏱ <i>скоро выдача</i>"
        elif phase_raw in ["LOOTING", "OPENED"]:
            status_line = f"🎁 <b>Лут готов</b> • <i>забирай лут прямо сейчас!</i>"
        elif phase_raw == "RUNNING":
            if time_sec > 0:
                status_line = f"⚔️ <b>Идет бой</b> • ⏱ <code>{time_str}</code>"
            else:
                status_line = f"⚔️ <b>Идет бой</b> • ⏱ <i>активен</i>"
        elif phase_raw in ["STARTING", "WAITING"]:
            if time_sec > 0:
                status_line = f"⏳ <b>{phase_name}</b> • ⏱ <code>{time_str}</code>"
            else:
                status_line = f"⏳ <b>{phase_name}</b> • <i>ожидание спавна</i>"
        else:
            status_line = f"{phase_icon} <b>{phase_name}</b>"
            
        # Build coords line
        if coords:
            coords_line = f"📍 <code>{coords}</code>"
        else:
            coords_line = "🔒 <i>Координаты ещё скрыты</i>"
            
        card = (
            f"<b>{i}. {icon} {name}</b>\n"
            f"   🏰 {server} (<code>{cmd}</code>)\n"
            f"   {status_line}\n"
            f"   {coords_line}"
        )
        cards.append(card)
        
    body = "\n\n".join(cards)
    footer = "\n\n━━━━━━━━━━━━━━━━━━━━\n💡 <i>Нажмите на команду сервера, чтобы скопировать её.</i>"
    return header + body + footer

def build_events_keyboard(page: int, total_pages: int, filter_mode: str) -> types.InlineKeyboardMarkup:
    """Builds inline navigation and filter keyboard."""
    builder = InlineKeyboardBuilder()
    
    # 1. Navigation buttons
    nav_buttons = []
    if page > 0:
        nav_buttons.append(
            types.InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data=f"events_page:{page - 1}:{filter_mode}"
            )
        )
    
    nav_buttons.append(
        types.InlineKeyboardButton(
            text=f"📄 {page + 1}/{max(1, total_pages)}",
            callback_data=f"events_noop"
        )
    )
    
    if page < total_pages - 1:
        nav_buttons.append(
            types.InlineKeyboardButton(
                text="Вперед ➡️",
                callback_data=f"events_page:{page + 1}:{filter_mode}"
            )
        )
    builder.row(*nav_buttons)
    
    # 2. Filter buttons
    all_btn = "🌐 Все" if filter_mode != "all" else "✅ Все"
    act_btn = "⚡ Активные" if filter_mode != "active" else "✅ Активные"
    up_btn = "⏳ Готовятся" if filter_mode != "upcoming" else "✅ Готовятся"
    
    builder.row(
        types.InlineKeyboardButton(text=all_btn, callback_data=f"events_page:0:all"),
        types.InlineKeyboardButton(text=act_btn, callback_data=f"events_page:0:active"),
        types.InlineKeyboardButton(text=up_btn, callback_data=f"events_page:0:upcoming")
    )
    
    # 3. Actions
    builder.row(
        types.InlineKeyboardButton(text="🔄 Обновить", callback_data=f"events_page:{page}:{filter_mode}"),
        types.InlineKeyboardButton(text="◀️ В меню", callback_data="main_menu")
    )
    
    return builder.as_markup()

def filter_event_list(events: list, filter_mode: str) -> list:
    """Filters events according to selected mode."""
    if filter_mode == "active":
        return [e for e in events if e["phase_raw"] in ["RUNNING", "ACTIVATING", "LOOTING", "OPENED"]]
    elif filter_mode == "upcoming":
        return [e for e in events if e["phase_raw"] in ["STARTING", "WAITING", "VOTING"]]
    return events

@router.message(Command("events"))
@router.message(F.text == "📦 Ивенты FunTime")
async def show_events_message(message: types.Message):
    wait_msg = await message.answer("🔄 <i>Загрузка актуальных ивентов с FunTime...</i>", parse_mode="HTML")
    try:
        raw_events = await fetch_funtime_events()
        filtered = filter_event_list(raw_events, "all")
        total_pages = max(1, math.ceil(len(filtered) / ITEMS_PER_PAGE))
        text = build_events_page_text(filtered, 0, total_pages, "all")
        kb = build_events_keyboard(0, total_pages, "all")
        await wait_msg.edit_text(text=text, parse_mode="HTML", reply_markup=kb)
    except Exception as e:
        await wait_msg.edit_text(
            f"❌ <b>Не удалось загрузить ивенты:</b>\n<code>{e}</code>\n\nПопробуйте позже.",
            parse_mode="HTML"
        )

@router.callback_query(F.data.startswith("events_page:"))
async def cb_events_page(callback: types.CallbackQuery):
    parts = callback.data.split(":")
    page = int(parts[1]) if len(parts) > 1 else 0
    filter_mode = parts[2] if len(parts) > 2 else "all"
    
    try:
        raw_events = await fetch_funtime_events()
        filtered = filter_event_list(raw_events, filter_mode)
        total_pages = max(1, math.ceil(len(filtered) / ITEMS_PER_PAGE))
        
        # Ensure page index in range
        if page >= total_pages:
            page = total_pages - 1
        if page < 0:
            page = 0
            
        text = build_events_page_text(filtered, page, total_pages, filter_mode)
        kb = build_events_keyboard(page, total_pages, filter_mode)
        
        await callback.message.edit_text(text=text, parse_mode="HTML", reply_markup=kb)
        await callback.answer()
    except Exception as e:
        await callback.answer("Ошибка обновления данных", show_alert=False)
        try:
            await callback.message.edit_text(
                f"❌ <b>Ошибка при загрузке:</b>\n<code>{e}</code>",
                parse_mode="HTML",
                reply_markup=build_events_keyboard(0, 1, filter_mode)
            )
        except Exception:
            pass

@router.callback_query(F.data == "events_noop")
async def cb_events_noop(callback: types.CallbackQuery):
    await callback.answer("Вы просматриваете эту страницу")
