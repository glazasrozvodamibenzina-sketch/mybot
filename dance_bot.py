import asyncio
from highrise import BaseBot, Position, AnchorPosition
from highrise.models import SessionMetadata, User

# Токен бота
BOT_TOKEN = "487cbb2ce20814c8a24c5845476385762501f1b87c1fb4be97817fbe491456dd"

# Полный список из 115 эмоций Highrise
EMOTES = [
    # 1 - 20 (Базовые и общение)
    "emote-wave", "emote-hello", "emote-yes", "emote-no", "emote-shy",
    "emote-tired", "emote-laughing", "emote-crying", "emote-sad", "emote-angry",
    "emote-kiss", "emote-bow", "emote-curtsy", "emote-thumbsup", "emote-clap",
    "emote-peace", "emote-flex", "emote-gasp", "emote-headache", "emote-disappointed",
    
    # 21 - 40 (Танцы)
    "emote-dance-tiktok8", "emote-dance-tiktok2", "dance-poptastic", "dance-pennywise", "emote-dance-shoppingcart",
    "emote-dance-russian", "emote-dance-blackpink", "emote-brainwash", "emote-punkdance", "emote-disco",
    "emote-vogue", "emote-shuffle", "emote-kpop", "emote-hiphop", "emote-samba",
    "emote-flamenco", "emote-salsa", "emote-robot", "emote-breakdance", "emote-twerk",
    
    # 41 - 60 (Необычные движения и трюки)
    "emote-hot", "emote-cold", "emote-snowangel", "emote-charge", "emote-snake",
    "emote-frog", "emote-superpose", "emote-cute", "emote-monster", "emote-zombierun",
    "emote-greedy", "emote-float", "emote-telekinesis", "emote-teleport", "emote-hero",
    "emote-model", "emote-fashion", "emote-jumpscare", "emote-savage", "emote-energy",
    
    # 61 - 80 (Позы и состояния)
    "emote-pose1", "emote-pose3", "emote-pose5", "emote-pose7", "emote-pose8",
    "idle-loop-sitfloor", "idle-loop-happy", "idle-sleepy", "idle-sad", "emote-confused",
    "emote-think", "emote-rest", "emote-hug", "emote-blush", "emote-embarrassed",
    "emote-singing", "emote-hyped", "emote-macarena", "emote-gangnam", "emote-rockstar",
    
    # 81 - 100 (Музыка, спорт и приколы)
    "emote-airguitar", "emote-violin", "emote-drums", "emote-swag", "emote-dab",
    "emote-boxer", "emote-karate", "emote-swordfight", "emote-magic", "emote-zombie",
    "emote-ghost", "emote-alien", "emote-dinosaur", "emote-chicken", "emote-bunny",
    "emote-cat", "emote-dog", "emote-fish", "emote-fly", "emote-fall",
    
    # 101 - 115 (Дополнительные позы)
    "emote-roll", "emote-spin", "emote-jump", "emote-cheer", "emote-salute",
    "emote-slap", "emote-facepalm", "emote-shrug", "emote-nod", "emote-wink",
    "emote-sleepy", "emote-giggle", "emote-sneeze", "emote-cough", "emote-yawn"
]

class EmotionBot(BaseBot):
    def __init__(self):
        super().__init__()
        self.current_emote = "emote-dance-tiktok8"
        self.loop_task = None

    async def on_start(self, session_metadata: SessionMetadata) -> None:
        print("Бот эмоций запущен и готов к работе!")
        if self.loop_task is None or self.loop_task.done():
            self.loop_task = asyncio.create_task(self.emote_loop())

    async def on_user_join(self, user: User, position: Position | AnchorPosition) -> None:
        total = len(EMOTES)
        try:
            await self.highrise.send_whisper(
                user.id, 
                f"Привет, {user.username}! Напиши в чат число от 1 до {total}, чтобы выбрать мою эмоцию!"
            )
        except Exception:
            await self.highrise.chat(
                f"Привет, @{user.username}! Напиши число от 1 до {total}, чтобы я показал эмоцию!"
            )

    async def on_chat(self, user: User, message: str) -> None:
        msg = message.strip()
        if msg.isdigit():
            num = int(msg)
            if 1 <= num <= len(EMOTES):
                selected_emote = EMOTES[num - 1]
                self.current_emote = selected_emote
                await self.highrise.send_emote(selected_emote)
                await self.highrise.chat(f"@{user.username} выбрал(а) эмоцию №{num}!")

    async def emote_loop(self):
        while True:
            try:
                if self.current_emote:
                    await self.highrise.send_emote(self.current_emote)
                await asyncio.sleep(9)
            except Exception as e:
                print(f"Ошибка в цикле эмоций: {e}")
                await asyncio.sleep(4)

if __name__ == "__main__":
    from highrise.__main__ import main
    # Запуск бота с указанным токеном
    main(EmotionBot(), BOT_TOKEN)
