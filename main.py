import asyncio
from highrise import BaseBot, User, Position
from highrise.main import main

class MyBot(BaseBot):
    def init(self):
        super().init()

    async def on_start(self, session_metadata: dict):
        print("Бот в сети! Захожу в комнату...")
        # Приветствие при входе самого бота
        await self.highrise.chat("Всем привет! Я бот-помощник. ✨")

    async def on_user_join(self, user: User, position: Position):
        # Приветствие игрока, который зашел в комнату
        print(f"Приветствую {user.username}")
        await self.highrise.chat(f"Добро пожаловать, {user.username}! Рады тебя видеть! ❤️")
        
        # Бот машет рукой игроку
        try:
            await self.highrise.send_emote("emote-hello", user.id)
        except Exception as e:
            print(f"Ошибка при выполнении эмоции: {e}")

if name == "main":
    # Твои данные для подключения
    room_id = "69ee35fab6bcfa4b70966bac"
    token = "93356fc362c144b1364b9b56314cd27400ad3d7737a7eeff88758290dbbae28d"
    
    bot = MyBot()
    asyncio.run(main([bot], room_id, token))
