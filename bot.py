import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import (
    Message, CallbackQuery, FSInputFile,
    InlineKeyboardMarkup, InlineKeyboardButton
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import (
    BOT_TOKEN, CLIENT_NAME, CLIENT_VERSION,
    CLIENT_SIZE, ADMIN_ID, SUPPORT_URL, JAR_FILE
)

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

stats = {"downloads": 0, "users": set()}


def main_menu():
    """Главное меню бота"""
    kb = InlineKeyboardBuilder()
    kb.button(text="📥 Скачать NightWare", callback_data="download")
    kb.button(text="ℹ️ Информация", callback_data="info")
    kb.button(text="💬 Поддержка", url=SUPPORT_URL)
    kb.adjust(1)
    return kb.as_markup()


def back_kb():
    """Кнопка возврата в главное меню"""
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="🏠 В главное меню", callback_data="back")
    ]])


@dp.message(Command("start"))
async def cmd_start(message: Message):
    stats["users"].add(message.from_user.id)
    text = (
        f"👋 <b>Привет, {message.from_user.first_name}!</b>\n\n"
        f"🌙 Это бот для скачивания мода <b>{CLIENT_NAME}</b>\n"
        f"📌 Версия: <b>{CLIENT_VERSION}</b>\n"
        f"💾 Размер: <b>{CLIENT_SIZE}</b>\n\n"
        f"Жми кнопку ниже 👇"
    )
    await message.answer(text, reply_markup=main_menu(), parse_mode="HTML")


@dp.callback_query(F.data == "download")
async def cb_download(callback: CallbackQuery):
    if not os.path.exists(JAR_FILE):
        await callback.answer("❌ Файл мода не найден", show_alert=True)
        return

    await callback.answer("⏳ Отправляю файл...")
    await callback.message.answer("📦 Подготавливаю файл, секунду...")

    try:
        file = FSInputFile(JAR_FILE, filename=JAR_FILE)
        await callback.message.answer_document(
            file,
            caption=(
                f"✅ <b>{CLIENT_NAME} готов!</b>\n\n"
                f"📌 Версия: <b>{CLIENT_VERSION}</b>\n"
                f"💾 Размер: <b>{CLIENT_SIZE}</b>\n\n"
                f"📂 <b>Как установить:</b>\n"
                f"1️⃣ Установи <b>Fabric Loader</b> для 1.21.4\n"
                f"   (fabricmc.net)\n"
                f"2️⃣ Скачай <b>Fabric API</b> для 1.21.4\n"
                f"   (modrinth.com/mod/fabric-api)\n"
                f"3️⃣ Кидай этот .jar и Fabric API в папку\n"
                f"   <code>.minecraft/mods</code>\n"
                f"4️⃣ Запусти игру через профиль <b>Fabric 1.21.4</b> 🎮\n\n"
                f"❓ Проблемы? → Поддержка"
            ),
            parse_mode="HTML",
            reply_markup=back_kb()
        )
        stats["downloads"] += 1
    except Exception as e:
        await callback.message.answer(f"❌ Ошибка: {e}")


@dp.callback_query(F.data == "info")
async def cb_info(callback: CallbackQuery):
    text = (
        f"📖 <b>О моде {CLIENT_NAME}</b>\n\n"
        f"🔹 Версия: <b>{CLIENT_VERSION}</b>\n"
        f"🔹 Загрузчик: <b>Fabric</b>\n"
        f"🔹 Размер: <b>{CLIENT_SIZE}</b>\n\n"
        f"📌 <b>Что нужно:</b>\n"
        f"1️⃣ Minecraft <b>1.21.4</b>\n"
        f"2️⃣ <b>Fabric Loader</b> 1.21.4\n"
        f"3️⃣ <b>Fabric API</b> в папке mods\n\n"
        f"📂 <b>Куда кидать моды:</b>\n"
        f"Win+R → <code>%appdata%\\.minecraft</code> → папка <b>mods</b>\n\n"
        f"❓ Проблемы? → Поддержка"
    )
    try:
        await callback.message.edit_text(
            text,
            reply_markup=back_kb(),
            parse_mode="HTML"
        )
    except Exception:
        await callback.message.answer(
            text,
            reply_markup=back_kb(),
            parse_mode="HTML"
        )
    await callback.answer()


@dp.callback_query(F.data == "back")
async def cb_back(callback: CallbackQuery):
    text = "🏠 <b>Главное меню</b>\n\nВыбери действие:"
    try:
        await callback.message.edit_text(
            text,
            reply_markup=main_menu(),
            parse_mode="HTML"
        )
    except Exception:
        # Если это документ (файл) — edit_text не сработает, отправляем новое
        await callback.message.answer(
            text,
            reply_markup=main_menu(),
            parse_mode="HTML"
        )
    await callback.answer()


@dp.message(Command("stats"))
async def cmd_stats(message: Message):
    if message.from_user.id != ADMIN_ID:
        return
    await message.answer(
        f"📊 <b>Статистика</b>\n\n"
        f"👥 Юзеров: <b>{len(stats['users'])}</b>\n"
        f"📥 Скачиваний: <b>{stats['downloads']}</b>",
        parse_mode="HTML"
    )


@dp.message(Command("menu"))
async def cmd_menu(message: Message):
    await message.answer(
        "🏠 <b>Главное меню</b>\n\nВыбери действие:",
        reply_markup=main_menu(),
        parse_mode="HTML"
    )


async def main():
    print(f"🤖 Бот {CLIENT_NAME} запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())