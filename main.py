import os
import asyncio
import random
from highrise import BaseBot, __main__
from highrise.models import SessionMetadata, User, Position

class MyBot(BaseBot):
    async def on_start(self, session_metadata: SessionMetadata) -> None:
        print("Бот-бармен успешно заступил на смену!")
        
        bot_position = Position(0.5, 0.0, 0.5, "FacingSouth") 
        try:
            await self.highrise.walk_to(bot_position)
        except Exception as e:
            print(f"Ошибка перемещения: {e}")

    async def on_user_join(self, user: User, position: Position | None = None) -> None:
        welcome_messages = [
            f"Добро пожаловать в наш бар, @{user.username}! 🍹 Присаживайся!",
            f"Приветствуем, @{user.username}! 🥂 Выбирай столик и отдыхай!",
            f"О, новый гость! Рады видеть тебя, @{user.username}! 🍸 Напиши !меню в чат!"
        ]
        await self.highrise.chat(random.choice(welcome_messages))

    async def on_chat(self, user: User, message: str) -> None:
        text = message.strip().lower()

        # Команда !меню
        if text == "!меню" or text == "!menu":
            await self.highrise.chat(f"@{user.username}, у нас в наличии: 🍹 !коктейль, 🍺 !пиво, ☕ !чай, 🍸 !шторм. Что тебе подать?")

        # Заказы напитков
        elif text == "!коктейль":
            drinks = ["Мартини с оливкой 🍸", "Тропический фреш 🍹", "Голубую Лагуну 🍹", "Мохито со льдом 🍹"]
            await self.highrise.chat(f"Держи твой {random.choice(drinks)}, @{user.username}! Приятного отдыха! ✨")

        elif text == "!пиво":
            await self.highrise.chat(f"Холодный пенный бокал уже у тебя, @{user.username}! 🍺 За счёт заведения!")

        elif text == "!чай" or text == "!кофе":
            await self.highrise.chat(f"Горячий напиток для уютного вечера подано, @{user.username}! ☕ Согревайся!")

        elif text == "!шторм":
            await self.highrise.chat(f"Ого, крепкий выбор! Спец-коктейль от бармена для @{user.username}! 🧪💥")

        # Ответ на простые приветствия
        elif text in ["привет", "прив", "хей", "hello", "hi"]:
            await self.highrise.chat(f"Привет-привет, @{user.username}! 👋 Заказывай что-нибудь из !меню!")

if __name__ == "__main__":
    room_id = os.getenv("ROOM_ID", "6851d25724cd01791ef3c7e2")
    token = os.getenv("BOT_TOKEN", "93356fc362c144b1364b9b56314cd27400ad3d7737a7eeff88758290dbbae28d")
    
    definitions = [__main__.BotDefinition(MyBot(), room_id, token)]
    asyncio.run(__main__.main(definitions))
