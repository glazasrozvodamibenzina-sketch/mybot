from highrise import BaseBot, User
from highrise.__main__ import main
import asyncio

class MyBot(BaseBot):
    async def on_chat(self, user: User, message: str) -> None:
        if message == "1":
            await self.highrise.send_emote("emote-lust", user.id)

if __name__ == "__main__":
    room_id = '6851d25724cd01791ef3c7e2'
    token = '6987046999e626661408c5ed1f3e5a151ba242fff2ed820c5df16bcfbe28bc67'
    asyncio.run(main(MyBot(), room_id, token))
