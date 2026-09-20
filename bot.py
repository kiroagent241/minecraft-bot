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
from aiogram.exceptions import TelegramForbiddenError, TelegramRetryAfter

from config import (
    BOT_TOKEN as CONFIG_TOKEN,
    CLIENT_NAME, CLIENT_VERSION,
    CLIENT_SIZE, ADMIN_ID, SUPPORT_URL, JAR_FILE
)
import database as db

BOT_TOKEN = os.getenv("BOT_TOKEN", CONFIG_TOKEN)

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

stats = {"downloads": 0}


def main_menu():
    kb = InlineKeyboardBuilder()
    kb.button(text="📥 Скачать NightWare", callback_data="download")
    kb.button(text="ℹ️ Информация", callback_data="info")
    kb.button(text="💬 Поддержка", url=SUPPORT_URL)
    kb.adjust(1)
    return kb.as_markup()


def back_kb():
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="🏠 В главное меню", callback_data="back")
    ]])


@dp.message(Command("start"))
async def cmd_start(message: Message):
    # Сохраняем юзера в БД
    await db.add_user(
        user_id=message.from_user.id,
        username=message.from_user.username or "",
        first_name=message.from_user.first_name or ""
    )

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
    count = await db.get_users_count()
    await message.answer(
        f"📊 <b>Статистика</b>\n\n"
        f"👥 Юзеров в БД: <b>{count}</b>\n"
        f"📥 Скачиваний за сессию: <b>{stats['downloads']}</b>",
        parse_mode="HTML"
    )


@dp.message(Command("menu"))
async def cmd_menu(message: Message):
    await message.answer(
        "🏠 <b>Главное меню</b>\n\nВыбери действие:",
        reply_markup=main_menu(),
        parse_mode="HTML"
    )


# ===== РАССЫЛКА =====

@dp.message(Command("broadcast"))
async def cmd_broadcast(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    # Получаем текст после /broadcast
    text = message.text.replace("/broadcast", "", 1).strip()

    if not text:
        await message.answer(
            "📢 <b>Как делать рассылку:</b>\n\n"
            "Напиши команду так:\n"
            "<code>/broadcast Привет, вышел новый мод!</code>\n\n"
            "Или отправь <b>в ответ</b> на любое сообщение (с картинкой/файлом) "
            "команду <code>/broadcast</code> — оно разошлётся всем.",
            parse_mode="HTML"
        )
        return

    users = await db.get_all_users()
    if not users:
        await message.answer("📭 В базе пока нет пользователей.")
        return

    status_msg = await message.answer(
        f"📢 Начинаю рассылку для <b>{len(users)}</b> юзеров...",
        parse_mode="HTML"
    )

    success = 0
    failed = 0

    for user_id in users:
        try:
            await bot.send_message(
                user_id,
                f"📢 <b>Сообщение от админа:</b>\n\n{text}",
                parse_mode="HTML"
            )
            success += 1
            await asyncio.sleep(0.05)  # защита от лимитов Telegram
        except TelegramForbiddenError:
            # Юзер заблокировал бота
            failed += 1
        except TelegramRetryAfter as e:
            # Превышен лимит — ждём сколько сказал Telegram
            await asyncio.sleep(e.retry_after)
            try:
                await bot.send_message(
                    user_id,
                    f"📢 <b>Сообщение от админа:</b>\n\n{text}",
                    parse_mode="HTML"
                )
                success += 1
            except Exception:
                failed += 1
        except Exception:
            failed += 1

    await status_msg.edit_text(
        f"✅ <b>Рассылка завершена!</b>\n\n"
        f"📨 Доставлено: <b>{success}</b>\n"
        f"❌ Не доставлено: <b>{failed}</b>",
        parse_mode="HTML"
    )


async def main():
    await db.init_db()
    print(f"🤖 Бот {CLIENT_NAME} запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())