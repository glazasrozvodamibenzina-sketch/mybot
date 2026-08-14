import asyncio
import random
from highrise import BaseBot, __main__
from highrise.models import SessionMetadata, User, Position

class MyBot(BaseBot):
    async def on_start(self, session_metadata: SessionMetadata) -> None:
        print("Бот-бармен успешно заступил на смену!")
        
        # Позиция бота в баре
        bot_position = Position(0.5, 0.0, 0.5, "FacingSouth") 
        try:
            await self.highrise.walk_to(bot_position)
        except Exception as e:
            print(f"Ошибка при перемещении бота: {e}")

    async def on_user_join(self, user: User, position: Position | None = None) -> None:
        # Уютные варианты приветствия для гостей бара
        welcome_messages = [
            f"Добро пожаловать в наш уютный бар, @{user.username}! 🍹 Присаживайся и устраивайся поудобнее!",
            f"Приветствуем в баре, @{user.username}! 🥂 Выбирай лучший столик и отдыхай!",
            f"О, новый гость! Рады видеть тебя, @{user.username}! 🍸 Отличного вечера!"
        ]
        await self.highrise.chat(random.choice(welcome_messages))

if __name__ == "__main__":
    room_id = "6851d25724cd01791ef3c7e2"
    token = "93356fc362c144b1364b9b56314cd27400ad3d7737a7eeff88758290dbbae28d"
    
    definitions = [__main__.BotDefinition(MyBot(), room_id, token)]
    asyncio.run(__main__.main(definitions))
