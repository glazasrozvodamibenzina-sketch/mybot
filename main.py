import asyncio
from highrise import BaseBot, User, Position
from highrise.main import main

class MyBot(BaseBot):
    async def on_start(self, session_metadata):
        print("✅ БОТ ВЫШЕЛ В ЭФИР!")
        await self.highrise.chat("Привет! Я новый бот. Пиши !пара или 1-50!")

    async def on_chat(self, user: User, message: str):
        if message.lower() == "!сюда":
            room_users = (await self.highrise.get_room_users()).content
            for u, pos in room_users:
                if u.id == user.id:
                    await self.highrise.teleport(self.id, pos)

if name == "main":
    room_id = "6851d25724cd01791ef3c7e2"
    token = "6987046999e626661408c5ed1f3e5a151ba242fff2ed820c5df16bcfbe28bc67"
    asyncio.run(main(MyBot(), room_id, token))
