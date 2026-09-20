import aiosqlite
from datetime import datetime, timedelta

DB_NAME = "users.db"


async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                language TEXT DEFAULT 'ru',
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                downloads INTEGER DEFAULT 0,
                last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.commit()


async def add_user(user_id: int, username: str, first_name: str, lang: str = "ru"):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            INSERT INTO users (user_id, username, first_name, language, last_active)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(user_id) DO UPDATE SET
                username = excluded.username,
                first_name = excluded.first_name,
                last_active = CURRENT_TIMESTAMP
        """, (user_id, username, first_name, lang))
        await db.commit()


async def get_lang(user_id: int) -> str:
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "SELECT language FROM users WHERE user_id = ?", (user_id,)
        )
        row = await cursor.fetchone()
        return row[0] if row else "ru"


async def set_lang(user_id: int, lang: str):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "UPDATE users SET language = ? WHERE user_id = ?", (lang, user_id)
        )
        await db.commit()


async def increment_downloads(user_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "UPDATE users SET downloads = downloads + 1 WHERE user_id = ?",
            (user_id,)
        )
        await db.commit()


async def get_all_users():
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT user_id FROM users")
        rows = await cursor.fetchall()
        return [row[0] for row in rows]


async def get_users_count():
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT COUNT(*) FROM users")
        row = await cursor.fetchone()
        return row[0] if row else 0


async def get_detailed_stats():
    """Возвращает подробную статистику"""
    async with aiosqlite.connect(DB_NAME) as db:
        # Всего юзеров
        cursor = await db.execute("SELECT COUNT(*) FROM users")
        total = (await cursor.fetchone())[0]

        # Новых за 24 часа
        cursor = await db.execute("""
            SELECT COUNT(*) FROM users 
            WHERE joined_at >= datetime('now', '-1 day')
        """)
        day = (await cursor.fetchone())[0]

        # Новых за 7 дней
        cursor = await db.execute("""
            SELECT COUNT(*) FROM users 
            WHERE joined_at >= datetime('now', '-7 days')
        """)
        week = (await cursor.fetchone())[0]

        # Новых за 30 дней
        cursor = await db.execute("""
            SELECT COUNT(*) FROM users 
            WHERE joined_at >= datetime('now', '-30 days')
        """)
        month = (await cursor.fetchone())[0]

        # Активных за 24ч
        cursor = await db.execute("""
            SELECT COUNT(*) FROM users 
            WHERE last_active >= datetime('now', '-1 day')
        """)
        active = (await cursor.fetchone())[0]

        # Всего скачиваний
        cursor = await db.execute("SELECT SUM(downloads) FROM users")
        downloads_row = await cursor.fetchone()
        downloads = downloads_row[0] if downloads_row[0] else 0

        # Топ-5 по скачиваниям
        cursor = await db.execute("""
            SELECT first_name, username, downloads 
            FROM users 
            ORDER BY downloads DESC 
            LIMIT 5
        """)
        top = await cursor.fetchall()

        return {
            "total": total,
            "day": day,
            "week": week,
            "month": month,
            "active": active,
            "downloads": downloads,
            "top": top,
        }