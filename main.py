import os
import json
import random
import asyncio
from highrise import BaseBot, __main__
from highrise.models import SessionMetadata, User, Position

# Файл для сохранения координат
POS_FILE = "welcome_pos.json"

# Разные варианты приветствий (можешь менять/добавлять фразы)
GREETINGS = [
    "Добро пожаловать в комнату, @{user}! ✨ Приятного времяпрепровождения!",
    "Рады тебя видеть, @{user}! 👋 Вливайся в тусовку!",
    "Привет, @{user}! 🎉 Чувствуй себя как дома!",
    "О, новый гость! Приветствую, @{user}! 💫",
    "Эй, @{user}! Рады твоему приходу! 💖"
]

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
                print(f"Ошибка чтения позиции: {e}")
        return None

    def save_position(self, pos: Position):
        """Сохранение координат в файл"""
        try:
            with open(POS_FILE, "w") as f:
                json.dump({"x": pos.x, "y": pos.y, "z": pos.z, "facing": pos.facing}, f)
        except Exception as e:
            print(f"Ошибка сохранения позиции: {e}")

    async def on_start(self, session_metadata: SessionMetadata) -> None:
        print("Приветственный бот запущен!")
        # Если есть сохраненная точка, сразу встаем на неё при запуске
        if self.saved_position:
            await asyncio.sleep(3)
            try:
                await self.highrise.walk_to(self.saved_position)
            except Exception as e:
                print(f"Ошибка перемещения при старте: {e}")

    async def on_user_join(self, user: User, position: Position | None = None) -> None:
        try:
            await asyncio.sleep(2)
            # Выбираем случайное приветствие
            greeting = random.choice(GREETINGS).format(user=user.username)
            await self.highrise.chat(greeting)
        except Exception as e:
            print(f"Ошибка приветствия: {e}")

    async def on_chat(self, user: User, message: str) -> None:
        try:
            text = message.strip().lower()

            # Отдельная команда для установки постоянного места
            if text in ["!welcomepos", "!встань"]:
                room_users = await self.highrise.get_room_users()
                for room_user, pos in room_users.content:
                    if room_user.id == user.id and isinstance(pos, Position):
                        self.saved_position = pos
                        self.save_position(pos)
                        await self.highrise.walk_to(pos)
                        await self.highrise.chat("Точка сохранена! Теперь я всегда буду стоять здесь! 📍")
                        break

        except Exception as e:
            print(f"Ошибка чата: {e}")

if __name__ == "__main__":
    # Вставь сюда данные Приветственного бота
    room_id = "6851d25724cd01791ef3c7e2"
    token = "ТВОЙ_ТОКЕН_ПРИВЕТСТВЕННОГО_БОТА"
    
    definitions = [__main__.BotDefinition(WelcomeBot(), room_id, token)]
    asyncio.run(__main__.main(definitions))
