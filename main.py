import random
import asyncio
from highrise import BaseBot, User, Position
from highrise.main import main

class MyBot(BaseBot):
    def init(self):
        super().init()
        self.pending_marriages = {} # Для хранения предложений

    async def on_start(self, session_metadata):
        print("Супер-Бот Знакомств запущен!")

    async def on_user_join(self, user: User, position):
        await self.highrise.chat(f"Привет, {user.username}! ✨ Напиши !пара, чтобы найти судьбу, или цифру 1-50 для танцев!")

    async def on_chat(self, user: User, message: str):
        msg = message.lower().strip()
        
        # 1. СИСТЕМА ЭМОЦИЙ (1-50)
        # Мы создаем список популярных эмоций. Если ввел цифру — бот подберет её.
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

        # 2. СИСТЕМА БРАКОВ
        if msg.startswith("!брак"):
            parts = message.split()
            if len(parts) < 2:
                await self.highrise.chat("Напиши: !брак @имя")
                return
            
            target_username = parts[1].replace("@", "")
            room_users = (await self.highrise.get_room_users()).content
            target_user = next((u for u, p in room_users if u.username.lower() == target_username.lower()), None)

            if target_user:
                if target_user.id == user.id:
                    await self.highrise.chat("Нельзя жениться на самом себе! 😂")
                    return
                self.pending_marriages[target_user.id] = {"proposer": user, "target": target_user}
                await self.highrise.chat(f"💍 {target_user.username}, @{user.username} предлагает тебе руку и сердце! Напиши 'да' или 'нет'")
            else:
                await self.highrise.chat("Игрок не найден в комнате.")

        elif msg == "да" and user.id in self.pending_marriages:
            proposer = self.pending_marriages[user.id]["proposer"]
            await self.highrise.chat(f"🎉 ГОРЬКО! @{proposer.username} и @{user.username} теперь муж и жена! ❤️🎊")
            await self.highrise.send_emote("emote-heartfingers", user.id)
            await self.highrise.send_emote("emote-heartfingers", proposer.id)
            del self.pending_marriages[user.id]

        elif msg == "нет" and user.id in self.pending_marriages:
            await self.highrise.chat("Разбитое сердце... Предложение отклонено. 💔")
            del self.pending_marriages[user.id]

        # 3. ПОИСК ПАРЫ (РАНДОМ)
        elif msg == "!пара":
            room_users = (await self.highrise.get_room_users()).content
            if len(room_users) < 2:
                await self.highrise.chat("В комнате слишком мало людей для поиска пары. Зови друзей! 1️⃣")
[26.04.2026 16:15] Прости. Прощай. Привет.#Фимозик: return
            
            potential_partner = random.choice([u for u, p in room_users if u.id != user.id])
            love_percent = random.randint(50, 100)
            await self.highrise.chat(f"🔮 Магия предсказала: @{user.username} и @{potential_partner.username} подходят друг другу на {love_percent}%! Идите обнимитесь! ❤️")

        # 4. ЛЮБОВЕМЕР
        elif msg.startswith("!любовь"):
            love_percent = random.randint(0, 100)
            await self.highrise.chat(f"❤️ Детектор любви показывает: {love_percent}%!")

        # Твоя старая команда !сюда
        elif msg == "!сюда":
            room_users = (await self.highrise.get_room_users()).content
            for u, pos in room_users:
                if u.id == user.id:
                    await self.highrise.teleport(self.id, pos)
                    break

if name == "main":
    main()
