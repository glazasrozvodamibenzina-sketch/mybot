import os
import asyncio
import random
from highrise import BaseBot, __main__
from highrise.models import SessionMetadata, User, Position

class MyBot(BaseBot):
    async def on_start(self, session_metadata: SessionMetadata) -> None:
        print("Бот успешно зашел в комнату!")

    async def on_user_join(self, user: User, position: Position | None = None) -> None:
        try:
            # Небольшая задержка, чтобы игрок успел прогрузиться в локации
            await asyncio.sleep(2)
            
            welcome_messages = [
                f"Добро пожаловать в наш бар, @{user.username}! 🍹 Присаживайся!",
                f"Приветствуем, @{user.username}! 🥂 Выбирай столик и отдыхай!",
                f"О, новый гость! Рады видеть тебя, @{user.username}! 🍸 Напиши !меню в чат!"
            ]
            await self.highrise.chat(random.choice(welcome_messages))
        except Exception as e:
            print(f"Ошибка при приветствии: {e}")

    async def on_chat(self, user: User, message: str) -> None:
        try:
            text = message.strip().lower()

            if text in ["!меню", "!menu"]:
                await self.highrise.chat(f"@{user.username}, у нас в наличии: 🍹 !коктейль, 🍺 !пиво, ☕ !чай, 🍸 !шторм.")

            elif text == "!коктейль":
                drinks = ["Мартини 🍸", "Тропический фреш 🍹", "Голубую Лагуну 🍹", "Мохито 🍹"]
                await self.highrise.chat(f"Держи твой {random.choice(drinks)}, @{user.username}! ✨")

            elif text == "!пиво":
                await self.highrise.chat(f"Холодный пенный бокал для @{user.username}! 🍺")

            elif text in ["!чай", "!кофе"]:
                await self.highrise.chat(f"Горячий напиток для @{user.username}! ☕")

            elif text == "!шторм":
                await self.highrise.chat(f"Спец-коктейль от бармена для @{user.username}! 🧪💥")

            elif text in ["привет", "прив", "хей", "hello", "hi"]:
                await self.highrise.chat(f"Привет, @{user.username}! 👋 Напиши !меню в чат!")
        except Exception as e:
            print(f"Ошибка в чате: {e}")

if __name__ == "__main__":
    room_id = os.getenv("ROOM_ID", "6851d25724cd01791ef3c7e2")
    token = os.getenv("BOT_TOKEN", "93356fc362c144b1364b9b56314cd27400ad3d7737a7eeff88758290dbbae28d")
    
    definitions = [__main__.BotDefinition(MyBot(), room_id, token)]
    asyncio.run(__main__.main(definitions))
