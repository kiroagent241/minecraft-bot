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
from aiogram.exceptions import (
    TelegramForbiddenError, TelegramRetryAfter, TelegramBadRequest
)

from config import (
    BOT_TOKEN as CONFIG_TOKEN,
    CLIENT_NAME, CLIENT_VERSION, CLIENT_SIZE,
    ADMIN_ID, SUPPORT_URL, JAR_FILE,
    CHANNEL_ID, CHANNEL_URL, DEFAULT_LANG
)
import database as db
from texts import t

BOT_TOKEN = os.getenv("BOT_TOKEN", CONFIG_TOKEN)

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# ===== ПРОВЕРКА ПОДПИСКИ =====

async def is_subscribed(user_id: int) -> bool:
    """Проверяет, подписан ли юзер на канал"""
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status in ("member", "administrator", "creator")
    except TelegramBadRequest:
        logging.warning("Не удалось проверить подписку. Проверь CHANNEL_ID!")
        return True
    except Exception as e:
        logging.error(f"Ошибка проверки подписки: {e}")
        return True


# ===== КЛАВИАТУРЫ =====

def main_menu(lang: str):
    kb = InlineKeyboardBuilder()
    kb.button(text=t(lang, "btn_download"), callback_data="download")
    kb.button(text=t(lang, "btn_info"), callback_data="info")
    kb.button(text=t(lang, "btn_lang"), callback_data="lang")
    kb.button(text=t(lang, "btn_support"), url=SUPPORT_URL)
    kb.adjust(1)
    return kb.as_markup()


def back_kb(lang: str):
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text=t(lang, "btn_back"), callback_data="back")
    ]])


def sub_kb(lang: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(lang, "btn_subscribe"), url=CHANNEL_URL)],
        [InlineKeyboardButton(text=t(lang, "btn_check_sub"), callback_data="check_sub")],
        [InlineKeyboardButton(text=t(lang, "btn_back"), callback_data="back")],
    ])


def lang_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="set_lang_ru")],
        [InlineKeyboardButton(text="🇬🇧 English", callback_data="set_lang_en")],
        [InlineKeyboardButton(text="🏠 Назад / Back", callback_data="back")],
    ])


# ===== ОСНОВНЫЕ КОМАНДЫ =====

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await db.add_user(
        user_id=message.from_user.id,
        username=message.from_user.username or "",
        first_name=message.from_user.first_name or "",
        lang=DEFAULT_LANG
    )
    lang = await db.get_lang(message.from_user.id)
    text = t(lang, "start",
             name=message.from_user.first_name,
             client=CLIENT_NAME,
             version=CLIENT_VERSION,
             size=CLIENT_SIZE)
    await message.answer(text, reply_markup=main_menu(lang), parse_mode="HTML")


@dp.message(Command("menu"))
async def cmd_menu(message: Message):
    lang = await db.get_lang(message.from_user.id)
    await message.answer(
        t(lang, "menu_title"),
        reply_markup=main_menu(lang),
        parse_mode="HTML"
    )


@dp.message(Command("help"))
async def cmd_help(message: Message):
    lang = await db.get_lang(message.from_user.id)
    if lang == "ru":
        text = (
            "❓ <b>Помощь</b>\n\n"
            "📥 <b>Как скачать мод:</b>\n"
            "1. Нажми «📥 Скачать NightWare»\n"
            "2. Подпишись на канал (если требуется)\n"
            "3. Получи файл\n\n"
            "🎮 <b>Как установить:</b>\n"
            "1. Установи <b>Fabric Loader</b> 1.21.4\n"
            "2. Скачай <b>Fabric API</b> 1.21.4\n"
            "3. Кидай .jar файлы в <code>.minecraft/mods</code>\n"
            "4. Запусти игру\n\n"
            "💬 <b>Проблемы?</b>\n"
            "Напиши в поддержку — кнопка в главном меню."
        )
    else:
        text = (
            "❓ <b>Help</b>\n\n"
            "📥 <b>How to download:</b>\n"
            "1. Press «📥 Download NightWare»\n"
            "2. Subscribe to the channel (if required)\n"
            "3. Get the file\n\n"
            "🎮 <b>How to install:</b>\n"
            "1. Install <b>Fabric Loader</b> 1.21.4\n"
            "2. Download <b>Fabric API</b> 1.21.4\n"
            "3. Put .jar files into <code>.minecraft/mods</code>\n"
            "4. Launch the game\n\n"
            "💬 <b>Issues?</b>\n"
            "Contact support — button in main menu."
        )
    await message.answer(text, parse_mode="HTML", reply_markup=back_kb(lang))


@dp.message(Command("lang"))
async def cmd_lang(message: Message):
    lang = await db.get_lang(message.from_user.id)
    await message.answer(
        t(lang, "lang_choose"),
        reply_markup=lang_kb(),
        parse_mode="HTML"
    )


# ===== CALLBACK-КНОПКИ =====

@dp.callback_query(F.data == "download")
async def cb_download(callback: CallbackQuery):
    lang = await db.get_lang(callback.from_user.id)

    if not await is_subscribed(callback.from_user.id):
        await callback.message.edit_text(
            t(lang, "sub_required"),
            reply_markup=sub_kb(lang),
            parse_mode="HTML"
        )
        await callback.answer()
        return

    if not os.path.exists(JAR_FILE):
        await callback.answer("❌ Файл мода не найден", show_alert=True)
        return

    await callback.answer("⏳")
    await callback.message.answer(t(lang, "preparing"))

    try:
        file = FSInputFile(JAR_FILE, filename=JAR_FILE)
        await callback.message.answer_document(
            file,
            caption=t(lang, "file_caption",
                      client=CLIENT_NAME,
                      version=CLIENT_VERSION,
                      size=CLIENT_SIZE),
            parse_mode="HTML",
            reply_markup=back_kb(lang)
        )
        await db.increment_downloads(callback.from_user.id)
    except Exception as e:
        await callback.message.answer(f"❌ Ошибка: {e}")


@dp.callback_query(F.data == "check_sub")
async def cb_check_sub(callback: CallbackQuery):
    lang = await db.get_lang(callback.from_user.id)

    if await is_subscribed(callback.from_user.id):
        await callback.message.edit_text(
            t(lang, "sub_success"),
            parse_mode="HTML"
        )
        if os.path.exists(JAR_FILE):
            file = FSInputFile(JAR_FILE, filename=JAR_FILE)
            await callback.message.answer_document(
                file,
                caption=t(lang, "file_caption",
                          client=CLIENT_NAME,
                          version=CLIENT_VERSION,
                          size=CLIENT_SIZE),
                parse_mode="HTML",
                reply_markup=back_kb(lang)
            )
            await db.increment_downloads(callback.from_user.id)
    else:
        await callback.answer(t(lang, "sub_failed"), show_alert=True)


@dp.callback_query(F.data == "info")
async def cb_info(callback: CallbackQuery):
    lang = await db.get_lang(callback.from_user.id)
    text = t(lang, "info",
             client=CLIENT_NAME,
             version=CLIENT_VERSION,
             size=CLIENT_SIZE)
    try:
        await callback.message.edit_text(
            text, reply_markup=back_kb(lang), parse_mode="HTML"
        )
    except Exception:
        await callback.message.answer(
            text, reply_markup=back_kb(lang), parse_mode="HTML"
        )
    await callback.answer()


@dp.callback_query(F.data == "back")
async def cb_back(callback: CallbackQuery):
    lang = await db.get_lang(callback.from_user.id)
    try:
        await callback.message.edit_text(
            t(lang, "menu_title"),
            reply_markup=main_menu(lang),
            parse_mode="HTML"
        )
    except Exception:
        await callback.message.answer(
            t(lang, "menu_title"),
            reply_markup=main_menu(lang),
            parse_mode="HTML"
        )
    await callback.answer()


@dp.callback_query(F.data == "lang")
async def cb_lang(callback: CallbackQuery):
    lang = await db.get_lang(callback.from_user.id)
    try:
        await callback.message.edit_text(
            t(lang, "lang_choose"),
            reply_markup=lang_kb(),
            parse_mode="HTML"
        )
    except Exception:
        await callback.message.answer(
            t(lang, "lang_choose"),
            reply_markup=lang_kb(),
            parse_mode="HTML"
        )
    await callback.answer()


@dp.callback_query(F.data.startswith("set_lang_"))
async def cb_set_lang(callback: CallbackQuery):
    new_lang = callback.data.replace("set_lang_", "")
    await db.set_lang(callback.from_user.id, new_lang)
    await callback.message.edit_text(
        t(new_lang, "lang_set"),
        reply_markup=main_menu(new_lang),
        parse_mode="HTML"
    )
    await callback.answer()


# ===== АДМИН-КОМАНДЫ =====

@dp.message(Command("stats"))
async def cmd_stats(message: Message):
    if message.from_user.id != ADMIN_ID:
        lang = await db.get_lang(message.from_user.id)
        await message.answer(t(lang, "no_access"))
        return

    s = await db.get_detailed_stats()

    text = (
        "📊 <b>РАСШИРЕННАЯ СТАТИСТИКА</b>\n\n"
        f"👥 Всего юзеров: <b>{s['total']}</b>\n"
        f"🔥 Активных за 24ч: <b>{s['active']}</b>\n\n"
        f"📈 <b>Новые юзеры:</b>\n"
        f"  • За 24 часа: <b>{s['day']}</b>\n"
        f"  • За 7 дней: <b>{s['week']}</b>\n"
        f"  • За 30 дней: <b>{s['month']}</b>\n\n"
        f"📥 Всего скачиваний: <b>{s['downloads']}</b>\n\n"
    )

    if s["top"]:
        text += "🏆 <b>Топ-5 по скачиваниям:</b>\n"
        for i, (first_name, username, downloads) in enumerate(s["top"], 1):
            name = first_name or "Без имени"
            uname = f" (@{username})" if username else ""
            text += f"  {i}. {name}{uname} — <b>{downloads}</b>\n"

    await message.answer(text, parse_mode="HTML")


@dp.message(Command("broadcast"))
async def cmd_broadcast(message: Message):
    if message.from_user.id != ADMIN_ID:
        lang = await db.get_lang(message.from_user.id)
        await message.answer(t(lang, "no_access"))
        return

    text = message.text.replace("/broadcast", "", 1).strip()

    if not text:
        await message.answer(
            "📢 <b>Как делать рассылку:</b>\n\n"
            "Напиши:\n"
            "<code>/broadcast Привет, вышел новый мод!</code>\n\n"
            "Или отправь <b>в ответ</b> на любое сообщение команду "
            "<code>/broadcast</code> — оно разошлётся всем.",
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
            lang = await db.get_lang(user_id)
            await bot.send_message(
                user_id,
                f"📢 <b>{'Сообщение от админа' if lang == 'ru' else 'Message from admin'}:</b>\n\n{text}",
                parse_mode="HTML"
            )
            success += 1
            await asyncio.sleep(0.05)
        except TelegramForbiddenError:
            failed += 1
        except TelegramRetryAfter as e:
            await asyncio.sleep(e.retry_after)
            try:
                await bot.send_message(user_id, text, parse_mode="HTML")
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


# ===== ЗАПУСК =====

async def main():
    await db.init_db()
    print(f"🤖 Бот {CLIENT_NAME} запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())