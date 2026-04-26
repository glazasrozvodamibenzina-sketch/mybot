import random
import asyncio
from highrise import BaseBot, User, Position
from highrise.__main__ import main

class MyBot(BaseBot):
    def __init__(self):
        super().__init__()
        self.pending_marriages = {}

    async def on_start(self, session_metadata):
        print("✅ Бот-Купидон успешно вошел в игру!")
        await self.highrise.chat("Я в эфире! ❤️ Ищешь любовь? Пиши !пара. Хочешь зажечь? Пиши цифру от 1 до 50!")

    async def on_user_join(self, user: User, position):
        await self.highrise.chat(f"Привет, {user.username}! ✨ Напиши !пара, чтобы найти свою судьбу!")

    async def on_chat(self, user: User, message: str):
        msg = message.lower().strip()
        
        # --- БЛОК ЭМОЦИЙ (1-50) ---
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
                await self.highrise.chat("Напиши: !брак @ник")
                return
            
            target_username = parts[1].replace("@", "")
            room_users = (await self.highrise.get_room_users()).content
            target_user = next((u for u, p in room_users if u.username.lower() == target_username.lower()), None)

            if target_user:
                if target_user.id == user.id:
                    await self.highrise.chat("Жениться на себе нельзя! 😂")
                    return
                self.pending_marriages[target_user.id] = {"proposer": user, "target": target_user}
                await self.highrise.chat(f"💍 @{target_user.username}, @{user.username} предлагает тебе брак! Напиши 'да' или 'нет' в чат!")
            else:
                await self.highrise.chat("Я не вижу этого игрока в комнате... 🕵️")

        elif msg == "да" and user.id in self.pending_marriages:
            proposer = self.pending_marriages[user.id]["proposer"]
            await self.highrise.chat(f"🎉 ГОРЬКО! @{proposer.username} и @{user.username} теперь официально пара! ❤️🎊")
            await self.highrise.send_emote("emote-heartfingers", user.id)
            await self.highrise.send_emote("emote-heartfingers", proposer.id)
            del self.pending_marriages[user.id]

        elif msg == "нет" and user.id in self.pending_marriages:
            await self.highrise.chat("💔 Предложение отклонено...")
            del self.pending_marriages[user.id]

        # --- ПОИСК ПАРЫ ---
        elif msg == "!пара":
            room_users = (await self.highrise.get_room_users()).content
            if len(room_users) < 2:
                await self.highrise.chat("Ждем гостей для поиска пары! 1️⃣")
                return
            
            partner = random.choice([u for u, p in room_users if u.id != user.id])
            love_percent = random.randint(60, 100)
            await self.highrise.chat(f"🔮 @{user.username} и @{partner.username} подходят друг другу на {love_percent}%! ❤️")

        # --- КОМАНДА ПРИЗЫВА (!сюда) ---
        elif msg == "!сюда":
            room_users = (await self.highrise.get_room_users()).content
            for u, pos in room_users:
                if u.id == user.id:
                    new_pos = Position(pos.x + 0.5, pos.y, pos.z)
                    await self.highrise.teleport(self.id, new_pos)
                    await self.highrise.chat("Я тут! ✨")
                    break

if __name__ == "__main__":
    room_id = "6851d25724cd01791ef3c7e2"
    token = "6987046999e626661408c5ed1f3e5a151ba242fff2ed820c5df16bcfbe28bc67"
    arun = main(MyBot(), room_id, token)
    asyncio.run(arun)
