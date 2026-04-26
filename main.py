import asyncio
import random
from highrise import BaseBot, User, Position
from highrise.models import SessionMetadata

# === НАСТРОЙКИ (CONFIG) ===
class config:
    prefix = '!'
    botID = '6987046999e626661408c5ed1f3e5a151ba242fff2ed820c5df16bcfbe28bc67' # Твой Токен сюда тоже можно
    ownerName = 'ТВОЙ_НИК'
    roomID = '6851d25724cd01791ef3c7e2'

# === ОСНОВНОЙ КОД БОТА ===
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
        print(f"✅ Бот {config.ownerName} запущен в комнате {config.roomID}")
        # Начальная позиция
        await self.highrise.teleport(self.id, Position(x=10, y=0, z=10, facing='EntityFacing.FrontRight'))

    async def on_user_join(self, user: User, position):
        await asyncio.sleep(1.5)
        await self.highrise.chat(f"🥂 Добро пожаловать в Бар, {user.username}! Пиши цифру (1-55) или '!налить'!")

    async def on_chat(self, user: User, message: str):
        msg = message.lower().strip()

        # Команда фиксации на месте
        if msg == f"{config.prefix}сюда":
            room_users = await self.highrise.get_room_users()
            for room_user, pos in room_users.content:
                if room_user.id == user.id:
                    await self.highrise.teleport(self.id, pos)
                    await self.highrise.chat(f"🫡 Пост принял!")
                    break

        # Эмоции 1-55
        if msg.isdigit():
            num = int(msg)
            if 1 <= num <= len(self.emotes_list):
                emote = self.emotes_list[num-1]
                self.dancing_users[user.id] = emote
                await self.highrise.chat(f"💃 Танцуем номер {num} (20 мин). Напиши '0', чтобы стоп.")
                asyncio.create_task(self.loop_emote(user.id, emote))
            elif num == 0:
                if user.id in self.dancing_users:
                    del self.dancing_users[user.id]
                    await self.highrise.chat(f"⏸️ {user.username} остановился.")

        # Бармен
        if msg == f"{config.prefix}налить":
            drinks = ["Коктейль 🍸", "Виски 🔥", "Сок 🍹", "Шампанское 🥂"]
            await self.highrise.chat(f"🍹 {user.username}, ваш {random.choice(drinks)} готов!")
            await self.highrise.send_emote("emote-lust", user.id)

        # Свадьбы
        if msg.startswith("брак с"):
            target_name = message.replace("брак с", "").strip().replace("@", "")
            room_users = await self.highrise.get_room_users()
            target_user = next((u for u, p in room_users.content if u.username.lower() == target_name.lower()), None)
            if target_user:
                self.proposals[target_user.id] = {"from": user.username, "to": target_user.username}
                await self.highrise.chat(f"💍 {target_user.username}, {user.username} зовет тебя замуж/жениться! Ответь 'Да' или 'Нет'")

        if msg == "да" and user.id in self.proposals:
            p = self.proposals[user.id]
            await self.highrise.chat(f"🎉 ГОРЬКО! {p['from']} и {p['to']} теперь пара! ❤️")
            await self.highrise.send_emote("emote-kiss", user.id)
            del self.proposals[user.id]

        # Разговоры
        if "как дела" in msg:
            await self.highrise.chat(f"Шикарно, {user.username}! Наливаю напитки!")

    async def loop_emote(self, user_id, emote):
        for _ in range(120):
            if user_id not in self.dancing_users or self.dancing_users[user_id] != emote:
                break
            try:
                await self.highrise.send_emote(emote, user_id)
            except:
                break
            await asyncio.sleep(10.5)
