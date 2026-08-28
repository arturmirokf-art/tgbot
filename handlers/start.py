from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

router = Router()

def get_main_inline_keyboard() -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text="📦 Ивенты FunTime",
            callback_data="events_page:0:all"
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text="🔍 Поиск похожей анки",
            callback_data="seed_search_menu"
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text="ℹ️ О боте / Инструкция",
            callback_data="bot_info"
        )
    )
    return builder.as_markup()

def get_main_reply_keyboard() -> types.ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(text="📦 Ивенты FunTime"),
        types.KeyboardButton(text="🔍 Поиск похожей анки")
    )
    return builder.as_markup(resize_keyboard=True)

WELCOME_TEXT = (
    "👋 <b>Добро пожаловать в FunTime Helper Bot!</b>\n\n"
    "⚡ <b>Доступные функции:</b>\n"
    "├ 📦 <b>Ивенты</b> — актуальные маяки, аирдропы, вулканы и сундуки с <code>funtime.me</code> в реальном времени с координатами и таймерами.\n"
    "└ 🔍 <b>Поиск похожей анки</b> — поиск серверов анархий с одинаковой сид-генерацией мира.\n\n"
    "👇 <i>Выберите действие в меню ниже:</i>"
)

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        text=WELCOME_TEXT,
        parse_mode="HTML",
        reply_markup=get_main_inline_keyboard()
    )

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    help_text = (
        "📖 <b>Справка по боту:</b>\n\n"
        "📦 <b>Ивенты:</b>\n"
        "• Данные обновляются в реальном времени с <code>https://funtime.me/events</code>.\n"
        "• Нажмите на кнопку «📦 Ивенты FunTime» для просмотра активных событий по 10 штук на странице.\n\n"
        "🔍 <b>Поиск похожих анархий:</b>\n"
        "• Отправьте номер анархии (например: <code>101</code> или <code>/seed 101</code>).\n"
        "• Бот найдет все сервера с такой же генерацией биомов и мира!\n"
        "• Чтобы записать новую анку в базу из игры, используйте команду в клиенте: <code>/seedft [номер]</code>\n"
    )
    await message.answer(text=help_text, parse_mode="HTML", reply_markup=get_main_inline_keyboard())

@router.callback_query(lambda c: c.data == "bot_info")
async def cb_bot_info(callback: types.CallbackQuery):
    await callback.answer()
    info_text = (
        "🤖 <b>FunTime Helper & Seed Matcher</b>\n\n"
        "💎 <b>Возможности:</b>\n"
        "• Мониторинг всех ивентов с сайта FunTime (Маяки, Аирдропы, Вулканы, Гейзеры)\n"
        "• Точные таймеры и координаты (X, Y, Z)\n"
        "• Быстрые команды подключения <code>/anarchy...</code>\n"
        "• Поиск анархий-близнецов по сид-генерации мира\n\n"
        "📌 <i>Бот работает 24/7 без задержек.</i>"
    )
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="◀️ В главное меню", callback_data="main_menu"))
    await callback.message.edit_text(text=info_text, parse_mode="HTML", reply_markup=builder.as_markup())

@router.callback_query(lambda c: c.data == "main_menu")
async def cb_main_menu(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        text=WELCOME_TEXT,
        parse_mode="HTML",
        reply_markup=get_main_inline_keyboard()
    )
