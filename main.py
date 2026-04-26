import asyncio
import random
import os
from highrise import BaseBot, User, Position
from highrise.models import SessionMetadata
from highrise.__main__ import main # Для автозапуска

# === ДАННЫЕ ДЛЯ ВХОДА ===
ROOM_ID = "6851d25724cd01791ef3c7e2"
API_TOKEN = "6987046999e626661408c5ed1f3e5a151ba242fff2ed820c5df16bcfbe28bc67"

class MyBot(BaseBot):
    def __init__(self):
        super().__init__()
        self.dancing_users = {} 
        self.proposals = {}    
        self.emotes_list = [
            "emote-kiss", "emote-no", "emote-sad", "emote-yes", "emote-laughing",
            "emote-hello", "emote-wave", "emote-shy", "emote-tired", "emoji-angry",
            "idle-loop-sitfloor", "emoji-thumbsup", "emote-lust", "emoji-cursing",
            "emote-greedy", "emoji-flex", "emoji-gagging", "emoji-celebrate",
            "dance-macarena", "dance-tiktok8", "dance-blackpink", "emote-model",
            "dance-tiktok2", "dance-pennywise", "emote-bow", "dance-russian",
            "emote-curtsy", "emote-snowball", "emote-hot", "emote-snowangel",
            "emote-charging", "dance-shoppingcart", "emote-confused", "idle-enthusiastic",
            "emote-telekinesis", "emote-float", "emote-teleporting", "emote-swordfight",
            "emote-maniac", "emote-energyball", "emote-snake", "idle-singing",
            "emote-frog", "emote-superpose", "emote-cute", "dance-tiktok9",
            "dance-weird", "dance-tiktok10", "emote-pose7", "emote-pose8",
            "idle-dance-casual", "emote-pose1", "emote-pose3", "emote-pose5", "emote-cutey"
        ]

    async def on_start(self, session_metadata: SessionMetadata):
        print("✅ БОТ В СЕТИ! Иди в комнату и проверяй.")
        await self.highrise.teleport(self.id, Position(x=10, y=0.5, z=10, facing='EntityFacing.FrontRight'))

    async def on_user_join(self, user: User, position):
        await asyncio.sleep(2)
        await self.highrise.chat(f"🥂 Привет, {user.username}! Танцуй (1-55), пей (!налить) или женись (брак с @имя)!")

    async def on_chat(self, user: User, message: str):
        msg = message.lower().strip()

        # Команда позвать бота к себе
        if msg == "!сюда":
            room_users = await self.highrise.get_room_users()
            for room_user, pos in room_users.content:
                if room_user.id == user.id:
                    await self.highrise.teleport(self.id, pos)
                    await self.highrise.chat(f"🫡 Я тут!")

        # Танцы по цифрам
        if msg.isdigit():
            num = int(msg)
            if 1 <= num <= len(self.emotes_list):
                emote = self.emotes_list[num-1]
                self.dancing_users[user.id] = emote
                await self.highrise.chat(f"💃 Танцуем # {num} (20 мин). Пиши '0' для стопа.")
                asyncio.create_task(self.loop_emote(user.id, emote))
            elif num == 0:
                if user.id in self.dancing_users:
                    del self.dancing_users[user.id]
                    await self.highrise.chat(f"⏸️ Стоп для {user.username}")

        # Бармен
        if msg == "!налить":
            drink = random.choice(["Мартини 🍸", "Виски 🥃", "Коктейль 🍹"])
            await self.highrise.chat(f"🍹 Держи свой {drink}, {user.username}!")
            await self.highrise.send_emote("emote-lust", user.id)

        # Свадьбы
        if msg.startswith("брак с"):
            target = message.replace("брак с", "").strip().replace("@", "")
            await self.highrise.chat(f"💍 {target}, тебе сделали предложение! Ответь 'Да' или 'Нет'")

        if msg == "да":
            await self.highrise.chat(f"🎉 ГОРЬКО! ❤️")
            await self.highrise.send_emote("emote-kiss", user.id)

    async def loop_emote(self, user_id, emote):
        for _ in range(120):
            if user_id not in self.dancing_users or self.dancing_users[user_id] != emote:
                break
            try: await self.highrise.send_emote(emote, user_id)
            except: break
            await asyncio.sleep(10.5)

# === ЭТА ЧАСТЬ ЗАПУСКАЕТ БОТА САМА ===
if __name__ == "__main__":
    import subprocess
    import sys
    
    # Авто-установка библиотеки, если её нет
    try:
        import highrise
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "highrise-bot-sdk"])
    
    # Запуск бота с твоими данными
    from highrise.__main__ import main
    sys.argv = ["highrise", "main:MyBot", ROOM_ID, API_TOKEN]
    main()
