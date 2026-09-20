# ===== ТЕКСТЫ ДЛЯ БОТА (RU / EN) =====

TEXTS = {
    "ru": {
        "start": (
            "👋 <b>Привет, {name}!</b>\n\n"
            "🌙 Это бот для скачивания мода <b>{client}</b>\n"
            "📌 Версия: <b>{version}</b>\n"
            "💾 Размер: <b>{size}</b>\n\n"
            "Жми кнопку ниже 👇"
        ),
        "btn_download": "📥 Скачать NightWare",
        "btn_info": "ℹ️ Информация",
        "btn_support": "💬 Поддержка",
        "btn_back": "🏠 В главное меню",
        "btn_subscribe": "📢 Подписаться на канал",
        "btn_check_sub": "✅ Я подписался",
        "btn_lang": "🌐 Язык",
        "menu_title": "🏠 <b>Главное меню</b>\n\nВыбери действие:",
        "sub_required": (
            "⚠️ <b>Для скачивания нужна подписка!</b>\n\n"
            "Подпишись на наш канал, потом нажми «Я подписался»."
        ),
        "sub_success": "✅ <b>Спасибо за подписку!</b>\n\nОтправляю файл...",
        "sub_failed": (
            "❌ <b>Ты ещё не подписан.</b>\n\n"
            "Подпишись на канал и попробуй снова."
        ),
        "preparing": "📦 Подготавливаю файл, секунду...",
        "file_caption": (
            "✅ <b>{client} готов!</b>\n\n"
            "📌 Версия: <b>{version}</b>\n"
            "💾 Размер: <b>{size}</b>\n\n"
            "📂 <b>Как установить:</b>\n"
            "1️⃣ Установи <b>Fabric Loader</b> для 1.21.4\n"
            "   (fabricmc.net)\n"
            "2️⃣ Скачай <b>Fabric API</b> для 1.21.4\n"
            "   (modrinth.com/mod/fabric-api)\n"
            "3️⃣ Кидай этот .jar и Fabric API в папку\n"
            "   <code>.minecraft/mods</code>\n"
            "4️⃣ Запусти игру через профиль <b>Fabric 1.21.4</b> 🎮\n\n"
            "❓ Проблемы? → Поддержка"
        ),
        "info": (
            "📖 <b>О моде {client}</b>\n\n"
            "🔹 Версия: <b>{version}</b>\n"
            "🔹 Загрузчик: <b>Fabric</b>\n"
            "🔹 Размер: <b>{size}</b>\n\n"
            "📌 <b>Что нужно:</b>\n"
            "1️⃣ Minecraft <b>1.21.4</b>\n"
            "2️⃣ <b>Fabric Loader</b> 1.21.4\n"
            "3️⃣ <b>Fabric API</b> в папке mods\n\n"
            "📂 <b>Куда кидать моды:</b>\n"
            "Win+R → <code>%appdata%\\.minecraft</code> → папка <b>mods</b>\n\n"
            "❓ Проблемы? → Поддержка"
        ),
        "lang_choose": "🌐 <b>Выбери язык:</b>",
        "lang_set": "✅ Язык изменён на русский",
        "no_access": "⛔ У тебя нет доступа к этой команде.",
    },
    "en": {
        "start": (
            "👋 <b>Hi, {name}!</b>\n\n"
            "🌙 This bot downloads the <b>{client}</b> mod\n"
            "📌 Version: <b>{version}</b>\n"
            "💾 Size: <b>{size}</b>\n\n"
            "Press the button below 👇"
        ),
        "btn_download": "📥 Download NightWare",
        "btn_info": "ℹ️ Info",
        "btn_support": "💬 Support",
        "btn_back": "🏠 Back to menu",
        "btn_subscribe": "📢 Subscribe to channel",
        "btn_check_sub": "✅ I subscribed",
        "btn_lang": "🌐 Language",
        "menu_title": "🏠 <b>Main menu</b>\n\nChoose an action:",
        "sub_required": (
            "⚠️ <b>Subscription required!</b>\n\n"
            "Subscribe to our channel, then press «I subscribed»."
        ),
        "sub_success": "✅ <b>Thanks for subscribing!</b>\n\nSending file...",
        "sub_failed": (
            "❌ <b>You're not subscribed yet.</b>\n\n"
            "Subscribe and try again."
        ),
        "preparing": "📦 Preparing file, one second...",
        "file_caption": (
            "✅ <b>{client} is ready!</b>\n\n"
            "📌 Version: <b>{version}</b>\n"
            "💾 Size: <b>{size}</b>\n\n"
            "📂 <b>How to install:</b>\n"
            "1️⃣ Install <b>Fabric Loader</b> for 1.21.4\n"
            "   (fabricmc.net)\n"
            "2️⃣ Download <b>Fabric API</b> for 1.21.4\n"
            "   (modrinth.com/mod/fabric-api)\n"
            "3️⃣ Put this .jar and Fabric API into\n"
            "   <code>.minecraft/mods</code>\n"
            "4️⃣ Launch game with <b>Fabric 1.21.4</b> profile 🎮\n\n"
            "❓ Issues? → Support"
        ),
        "info": (
            "📖 <b>About {client}</b>\n\n"
            "🔹 Version: <b>{version}</b>\n"
            "🔹 Loader: <b>Fabric</b>\n"
            "🔹 Size: <b>{size}</b>\n\n"
            "📌 <b>Requirements:</b>\n"
            "1️⃣ Minecraft <b>1.21.4</b>\n"
            "2️⃣ <b>Fabric Loader</b> 1.21.4\n"
            "3️⃣ <b>Fabric API</b> in mods folder\n\n"
            "📂 <b>Mods folder:</b>\n"
            "Win+R → <code>%appdata%\\.minecraft</code> → <b>mods</b>\n\n"
            "❓ Issues? → Support"
        ),
        "lang_choose": "🌐 <b>Choose language:</b>",
        "lang_set": "✅ Language changed to English",
        "no_access": "⛔ You don't have access to this command.",
    },
}


def t(lang: str, key: str, **kwargs) -> str:
    """Получить текст по языку и ключу"""
    text = TEXTS.get(lang, TEXTS["ru"]).get(key, "")
    if kwargs:
        return text.format(**kwargs)
    return text