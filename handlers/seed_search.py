from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from services.seed_db import find_similar_anarchies, load_all_seeds

router = Router()

class SeedSearchState(StatesGroup):
    waiting_for_anarchy = State()

def get_search_keyboard() -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="🔍 Искать другую анку", callback_data="seed_search_menu"))
    builder.row(types.InlineKeyboardButton(text="◀️ В главное меню", callback_data="main_menu"))
    return builder.as_markup()

@router.message(Command("seed"))
@router.message(F.text == "🔍 Поиск похожей анки")
@router.callback_query(F.data == "seed_search_menu")
async def start_seed_search(event: types.Message | types.CallbackQuery, state: FSMContext):
    await state.set_state(SeedSearchState.waiting_for_anarchy)
    
    seeds = load_all_seeds()
    count = len(seeds)
    
    text = (
        "🔍 <b>Поиск похожей анархии по сид-генерации</b>\n\n"
        f"📊 В базе сейчас: <b>{count}</b> записанных анархий.\n\n"
        "💬 <b>Отправьте номер анархии</b> (например: <code>101</code> или <code>203</code>):\n"
        "<i>Бот найдет все сервера с точно такой же генерацией биомов и мира!</i>"
    )
    
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="◀️ В главное меню", callback_data="main_menu"))
    
    if isinstance(event, types.CallbackQuery):
        await event.answer()
        await event.message.edit_text(text=text, parse_mode="HTML", reply_markup=builder.as_markup())
    else:
        # Check if argument was passed in command: e.g. /seed 101
        args = event.text.split()
        if len(args) > 1 and args[1].isdigit():
            await process_seed_query(event, args[1], state)
            return
        await event.answer(text=text, parse_mode="HTML", reply_markup=builder.as_markup())

@router.message(SeedSearchState.waiting_for_anarchy)
async def process_anarchy_input(message: types.Message, state: FSMContext):
    query = message.text.strip()
    await process_seed_query(message, query, state)

async def process_seed_query(message: types.Message, query: str, state: FSMContext):
    clean_query = query.replace("anarchy", "").replace("анка", "").replace("анархия", "").strip()
    
    if not clean_query:
        await message.answer("⚠️ Пожалуйста, введите корректный номер анархии (например: <code>101</code>).", parse_mode="HTML")
        return
        
    result = find_similar_anarchies(clean_query)
    
    if not result["found"]:
        text = (
            f"❌ <b>Анархия {clean_query} не найдена в базе!</b>\n\n"
            "ℹ️ <i>Эта анархия ещё не была записана.</i>\n\n"
            "📌 <b>Как добавить сид-генерацию в базу?</b>\n"
            f"1. Зайдите на сервер анархии <b>{clean_query}</b> в игре.\n"
            f"2. Напишите в чат команду: <code>/seedft {clean_query}</code>\n"
            "3. Клиент автоматически запишет генерацию в общую базу!"
        )
        await message.answer(text=text, parse_mode="HTML", reply_markup=get_search_keyboard())
        await state.clear()
        return

    seed = result["seed"]
    matching = result["matching"]
    
    if matching:
        match_lines = []
        for ank in matching:
            match_lines.append(f"• <b>Анархия {ank}</b> — <code>/anarchy{ank}</code>")
        match_text = "\n".join(match_lines)
        
        response = (
            f"🎯 <b>Результаты поиска для Анархии {clean_query}:</b>\n\n"
            f"🧬 <b>Сид-генерация мира:</b> <code>{seed}</code>\n\n"
            f"✨ <b>Найдены сервера-близнецы с такой же генерацией ({len(matching)}):</b>\n"
            f"{match_text}\n\n"
            "💡 <i>На этих анархиях полностью совпадает генерация дикого мира, расположение биомов, руд и структур!</i>"
        )
    else:
        response = (
            f"📍 <b>Информация по Анархии {clean_query}:</b>\n\n"
            f"🧬 <b>Сид-генерация мира:</b> <code>{seed}</code>\n\n"
            "ℹ️ <i>Пока это единственная анархия с таким сидом в базе.</i>\n"
            "Записывайте другие анархии командой <code>/seedft [номер]</code> в игре, чтобы находить новые совпадения!"
        )
        
    await message.answer(text=response, parse_mode="HTML", reply_markup=get_search_keyboard())
    await state.clear()

# Also support direct number messages (e.g. user simply sends "101" anytime)
@router.message(F.text.regexp(r'^(?:anarchy\s*|анка\s*|анархия\s*)?(\d{1,4})$'))
async def handle_direct_anarchy_number(message: types.Message, state: FSMContext):
    match = message.text.strip()
    await process_seed_query(message, match, state)
