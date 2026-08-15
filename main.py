import os
import json
import random
import asyncio

from highrise import BaseBot, __main__, User
from highrise.models import SessionMetadata, Position
from highrise.__main__ import BotDefinition


# ==========================================
# НАСТРОЙКИ
# ==========================================

ROOM_ID = "6851d25724cd01791ef3c7e2"
TOKEN = "93356fc362c144b1364b9b56314cd27400ad3d7737a7eeff88758290dbbae28d"
POS_FILE = "welcome_pos.json"

GREETINGS = [
    "Добро пожаловать, @{user}! ✨ Приятного времяпрепровождения!",
    "Рады тебя видеть, @{user}! 👋 Вливайся в нашу тусовку!",
    "Привет, @{user}! 🎉 Чувствуй себя как дома!",
    "О, новый гость! Привет, @{user}! 💫",
    "Эй, @{user}! 💖 Рады твоему приходу!"
]


# ==========================================
# ПРИВЕТСТВЕННЫЙ БОТ
# ==========================================

class WelcomeBot(BaseBot):

    def __init__(self):
        super().__init__()
        self.saved_position = self.load_position()

    def load_position(self) -> Position | None:
        """Загрузка сохраненных координат из файла"""
        if os.path.exists(POS_FILE):
            try:
                with open(POS_FILE, "r") as f:
                    data = json.load(f)
                    return Position(data["x"], data["y"], data["z"], data.get("facing", "FrontRight"))
            except Exception as e:
                print(f"❌ Ошибка чтения позиции: {e}")
        return None

    def save_position(self, pos: Position):
        """Сохранение координат в файл"""
        try:
            with open(POS_FILE, "w") as f:
                json.dump({"x": pos.x, "y": pos.y, "z": pos.z, "facing": pos.facing}, f)
        except Exception as e:
            print(f"❌ Ошибка сохранения позиции: {e}")

    async def on_start(self, session_metadata: SessionMetadata):
        print("✅ Приветственный бот запущен!")
        print(f"🏠 Комната: {ROOM_ID}")
        
        # Если точка сохранена, встаем на нее при запуске
        if self.saved_position:
            await asyncio.sleep(3)
            try:
                await self.highrise.walk_to(self.saved_position)
            except Exception as e:
                print(f"❌ Ошибка перемещения при старте: {e}")

    async def on_user_join(self, user: User, position: Position | None = None):
        try:
            await asyncio.sleep(2)
            greeting = random.choice(GREETINGS).replace("@{user}", f"@{user.username}")
            await self.highrise.chat(greeting)
            print(f"👋 Новый пользователь: {user.username}")
        except Exception as e:
            print(f"❌ Ошибка приветствия: {e}")

    async def on_chat(self, user: User, message: str) -> None:
        try:
            text = message.strip().lower()

            # Команда для установки точки спавна бота
            if text in ["!welcomepos", "!встань"]:
                room_users = await self.highrise.get_room_users()
                for room_user, pos in room_users.content:
                    if room_user.id == user.id and isinstance(pos, Position):
                        self.saved_position = pos
                        self.save_position(pos)
                        await self.highrise.walk_to(pos)
                        await self.highrise.chat("Точка сохранена! Теперь я буду стоять здесь! 📍")
                        break
        except Exception as e:
            print(f"❌ Ошибка чата: {e}")


# ==========================================
# ЗАПУСК БОТА
# ==========================================

if __name__ == "__main__":
    definitions = [
        BotDefinition(
            WelcomeBot(),
            ROOM_ID,
            TOKEN
        )
    ]

    asyncio.run(
        __main__.main(definitions)
    )
