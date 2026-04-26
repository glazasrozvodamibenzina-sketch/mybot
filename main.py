import random
import asyncio
from highrise import BaseBot, User, Position, AnchorPosition
from highrise.__main__ import main

class MyBot(BaseBot):
    def __init__(self):
        super().__init__()
        self.pending_marriages = {}

    async def on_start(self, session_metadata):
        print("Бот Купидон запущен!")
        # Бот напишет это, как только появится в комнате
        await self.highrise.chat("Я в эфире и готов венчать сердца! ❤️ Пиши !пара или !брак @ник")

    async def on_user_join(self, user: User, position):
        greetings = [
            f"Привет, {user.username}! Ищешь пару? Пиши !пара ✨",
            f"Добро пожаловать, {user.username}! Напиши цифру от 1 до 50, чтобы я станцевал! 💃"
        ]
        await self.highrise.chat(random.choice(greetings))

    async def on_chat(self, user: User, message: str):
        msg = message.lower().strip()
        
        # --- 50 ЭМОЦИЙ ---
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

        if msg.isdigit():
            num = int(msg)
            if 1 <= num <= 50:
                await self.highrise.send_emote(all_emotes[num-1], user.id)

        # --- СИСТЕМА БРАКОВ ---
        if msg.startswith("!брак"):
            parts = message.split()
            if len(parts) < 2:
                await self.highrise.chat("Напиши: !брак @имя")
                return
            
            target_username = parts[1].replace("@", "")
            room_users = (await self.highrise.get_room_users()).content
            target_user = next((u for u, p in room_users if u.username.lower() == target_username.lower()), None)

            if target_user:
                self.pending_marriages[target_user.id] = {"proposer": user, "target": target_user}
                await self.highrise.chat(f"💍 {target_user.username}, тебе предложили брак! Пиши 'да' или 'нет'")
            else:
                await self.highrise.chat("Игрок не найден.")

        elif msg == "да" and user.id in self.pending_marriages:
            proposer = self.pending_marriages[user.id]["proposer"]
            await self.highrise.chat(f"🎉 ГОРЬКО! @{proposer.username} и @{user.username} теперь пара! ❤️")
            await self.highrise.send_emote("emote-heartfingers", user.id)
            del self.pending_marriages[user.id]

        # --- ПОИСК ПАРЫ ---
        elif msg == "!пара":
            room_users = (await self.highrise.get_room_users()).content
            if len(room_users) > 1:
                partner = random.choice([u for u, p in room_users if u.id != user.id])
                await self.highrise.chat(f"🔮 Судьба шепчет: @{user.username} и @{partner.username} — идеальная пара! ❤️")

        # --- КОМАНДА ПРИЗЫВА ---
        elif msg == "!сюда":
            room_users = (await self.highrise.get_room_users()).content
            for u, pos in room_users:
                if u.id == user.id:
                    await self.highrise.teleport(self.id, pos)
                    break

if __name__ == "__main__":
    # ВОТ ТУТ МЫ ПРОПИСЫВАЕМ ТВОИ ДАННЫЕ
    # Замени 'ТВОЙ_ТОКЕН_ТУТ' на свой токен, если он не подхватится из Render
    import os
    room_id = "6851d25724cd01791ef3c7e2" 
    token = os.environ.get("api_token") 
    arun = main(MyBot(), room_id, token)
    asyncio.run(arun)
