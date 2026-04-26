import random
import sys
from highrise import BaseBot, User, Position
from highrise.__main__ import main

class MyBot(BaseBot):
    async def on_start(self, session_metadata):
        print("Радио-бот в эфире!")
        await self.highrise.teleport(self.id, Position(x=10, y=0, z=10, facing='EntityFacing.FrontRight'))

    async def on_user_join(self, user: User, position):
        await self.highrise.chat(f"Привет, {user.username}! Напиши 1 или 2, чтобы я зажег!")

    async def on_chat(self, user: User, message: str):
        msg = message.lower().strip()
        
        if msg == "1":
            await self.highrise.send_emote("dance-breakdance", user.id)
        elif msg == "2":
            # Тот самый танец
            await self.highrise.send_emote("dance-sexy", user.id)
        elif msg == "0":
            await self.highrise.send_emote("idle-loop-sitfloor", user.id)
        
        elif msg == "!сюда":
            room_users = await self.highrise.get_room_users()
            for room_user, pos in room_users.content:
                if room_user.id == user.id:
                    await self.highrise.teleport(self.id, pos)
                    await self.highrise.chat("Принято! 🫡")
                    break

if __name__ == "__main__":
    main()
