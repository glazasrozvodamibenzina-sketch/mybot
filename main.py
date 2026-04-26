import random
import asyncio
from highrise import BaseBot, User, Position
from highrise.main import main

class MyBot(BaseBot):
    def init(self):
        super().init()
        self.pending_marriages = {}

    async def on_start(self, session_metadata):
        print("✅ БОТ ВЫШЕЛ В ЭФИР!")
        await self.highrise.chat("Я вернулся! ❤️ Новый ключ — новая жизнь! Пиши !пара или !брак @ник")

    async def on_user_join(self, user: User, position):
        await self.highrise.chat(f"Привет, {user.username}! ✨ Пиши !пара, чтобы найти любовь, или цифру 1-50 для танцев!")

    async def on_chat(self, user: User, message: str):
        msg = message.lower().strip()
        
        # --- ТАНЦЫ (1-50) ---
        all_emotes = [
            "dance-breakdance", "dance-sexy", "dance-pancakes", "dance-tiktok8", "emote-skating",
            "dance-eboy", "dance-blackpink", "dance-shoppingcart", "emote-bow", "emote-curtsy",
            "dance-anime", "dance-duckwalk", "emote-confused", "emote-ghosty", "emote-heartfingers",
            "emote-hot", "emote-judging", "emote-kpop", "emote-laughing", "emote-lust",
            "emote-muddy", "emote-pose1", "emote-pose3", "emote-pose5", "emote-pose7",
            "emote-pose8", "emote-shy", "emote-snake", "emote-snowangel", "emote-snowball",
            "emote-superpose", "emote-telekinesis", "emote-teleporting", "emote-think", "emote-thumbsup",
            "emote-tired", "emote-wave", "emote-zombie", "idle-dance-casual", "idle-loop-sitfloor",
            "dance-russian", "dance-voguehands", "emote-gravity", "emote-headache", "emote-icecream",
            "emote-relic", "emote-robot", "emote-sleigh", "emote-wings", "emote-boxer"
        ]
        if msg.isdigit() and 1 <= int(msg) <= 50:
            await self.highrise.send_emote(all_emotes[int(msg)-1], user.id)

        # --- СУДЬБА / ПАРА ---
        elif msg == "!пара":
            room_users = (await self.highrise.get_room_users()).content
            if len(room_users) > 1:
                partner = random.choice([u for u, p in room_users if u.id != user.id])
                await self.highrise.chat(f"🔮 Предсказание для @{user.username}: твоя идеальная пара сегодня — @{partner.username}! ❤️")
            else:
                await self.highrise.chat("В комнате никого нет... Позови друзей! 😊")

        # --- ТЕЛЕПОРТ ---
        elif msg == "!сюда":
            room_users = (await self.highrise.get_room_users()).content
            for u, pos in
