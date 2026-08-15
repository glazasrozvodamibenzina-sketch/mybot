import os
import asyncio
from highrise import BaseBot, __main__
from highrise.models import SessionMetadata, User, Position

# Полный список 100% рабочих эмоций и танцев Highrise
EMOTE_MAP = {
    # Танцы (1 - 40)
    "1": "idle-dance-casual", "2": "dance-single-1", "3": "dance-shoppingcart", 
    "4": "dance-russian", "5": "dance-macarena", "6": "dance-weird", "7": "dance-tiktok2", 
    "8": "dance-tiktok8", "9": "dance-blackpink", "10": "dance-pennypacker", "11": "dance-metal", 
    "12": "dance-floss", "13": "dance-duckwalk", "14": "dance-breakdance", "15": "dance-orangejustice", 
    "16": "dance-sicko", "17": "dance-smoothwalk", "18": "dance-vogueing", "19": "dance-zombie",
    "20": "dance-gangnam", "21": "dance-handsup", "22": "dance-aerobics", "23": "dance-frog", 
    "24": "dance-bunnyhop", "25": "dance-techno", "26": "dance-disco", "27": "dance-samba", 
    "28": "dance-salsa", "29": "dance-twerk", "30": "dance-belly", "31": "dance-tap", 
    "32": "dance-hiphop", "33": "dance-kpop", "34": "dance-robot", "35": "dance-shuffle", 
    "36": "dance-rock", "37": "dance-swing", "38": "dance-waltz", "39": "dance-chacha",
    "40": "dance-icecream",

    # Эмоции и движения (41 - 90)
    "41": "emote-yes", "42": "emote-no", "43": "emote-sad", "44": "emote-laughing", 
    "45": "emote-nevergonna", "46": "emote-wave", "47": "emote-tired", "48": "emote-shy", 
    "49": "emote-angry", "50": "emote-think", "51": "emote-clap", "52": "emote-bow", 
    "53": "emote-curtsy", "54": "emote-peace", "55": "emote-flex", "56": "emote-dab", 
    "57": "emote-facepalm", "58": "emote-headache", "59": "emote-bored", "60": "emote-sleepy",
    "61": "emote-confused", "62": "emote-roll", "63": "emote-kiss", "64": "emote-hug", 
    "65": "emote-crying", "66": "emote-scared", "67": "emote-disgusted", "68": "emote-surprised", 
    "69": "emote-blushing", "70": "emote-smirk", "71": "emote-hero", "72": "emote-superhero", 
    "73": "emote-villain", "74": "emote-zombierun", "75": "emote-ninja", "76": "emote-sword", 
    "77": "emote-magic", "78": "emote-teleport", "79": "emote-levitate", "80": "emote-fly", 
    "81": "emote-backflip", "82": "emote-frontflip", "83": "emote-cartwheel", "84": "emote-handstand", 
    "85": "emote-split", "86": "emote-kick", "87": "emote-punch", "88": "emote-block", 
    "89": "emote-dodge", "90": "emote-victory"
}

class DanceBot(BaseBot):
    def __init__(self):
        super().__init__()
        self.active_dances = {}

    async def on_start(self, session_metadata: SessionMetadata) -> None:
        print("Дэнс-бот запущен!")

    async def on_user_join(self, user: User, position: Position | None = None) -> None:
        try:
            await asyncio.sleep(2)
            await self.highrise.chat(f"Привет, @{user.username}! 💃 Напиши в чат цифру от 1 до 90 для танца! (Стоп — напиши 0)")
        except Exception as e:
            print(f"Ошибка приветствия: {e}")

    async def on_user_leave(self, user: User) -> None:
        if user.id in self.active_dances:
            self.active_dances[user.id].cancel()
            del self.active_dances[user.id]

    async def loop_emote(self, user_id: str, emote_id: str):
        try:
            while True:
                res = await self.highrise.send_emote(emote_id, user_id)
                # Если сервер вернул ошибку, что эмоция недоступна
                if not res:
                    break
                await asyncio.sleep(8)
        except asyncio.CancelledError:
            pass
        except Exception as e:
            print(f"Ошибка при проигрывании эмоции: {e}")

    async def on_chat(self, user: User, message: str) -> None:
        try:
            text = message.strip().lower()

            # Остановка
            if text in ["0", "stop", "стоп"]:
                if user.id in self.active_dances:
                    self.active_dances[user.id].cancel()
                    del self.active_dances[user.id]
                    await self.highrise.chat(f"@{user.username}, танец остановлен! 🛑")
                return

            # Включение движения
            if text in EMOTE_MAP:
                if user.id in self.active_dances:
                    self.active_dances[user.id].cancel()
                
                emote_id = EMOTE_MAP[text]
                task = asyncio.create_task(self.loop_emote(user.id, emote_id))
                self.active_dances[user.id] = task

            # Позиционирование
            if text == "!topos":
                room_users = await self.highrise.get_room_users()
                for room_user, pos in room_users.content:
                    if room_user.id == user.id and isinstance(pos, Position):
                        await self.highrise.walk_to(Position(pos.x, pos.y, pos.z, pos.facing))
                        await self.highrise.chat("Встал сюда! 📍")
                        break

        except Exception as e:
            print(f"Ошибка чата: {e}")

if __name__ == "__main__":
    room_id = "6851d25724cd01791ef3c7e2"
    token = "487cbb2ce20814c8a24c5845476385762501f1b87c1fb4be97817fbe491456dd"
    
    definitions = [__main__.BotDefinition(DanceBot(), room_id, token)]
    asyncio.run(__main__.main(definitions))
