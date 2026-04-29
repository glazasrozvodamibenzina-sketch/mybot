import random
import asyncio
from highrise import BaseBot, User
from highrise.__main__ import main

class WelcomeBot(BaseBot):
    async def on_start(self, session_metadata):
        print("✅ Бот-Приветствие запущен в новой комнате!")

    async def on_user_join(self, user: User, position):
        # Разнообразные фразы для комнаты знакомств
        greetings = [
            f"Привет, {user.username}! Добро пожаловать в комнату знакомств! 🌸",
            f"Рады тебя видеть, {user.username}! Не стесняйся общаться! ✨",
            f"Приветик, {user.username}! Надеемся, ты найдешь здесь приятную компанию. 💖",
            f"Добро пожаловать, {user.username}! Расскажи, как твое настроение? 👋",
            f"О, новый гость! {user.username}, заходи, присаживайся! 😊",
            f"Привет! {user.username}, здесь все свои, располагайся! 🏠",
            f"Хей, {user.username}! Ищешь новые знакомства? Ты в правильном месте! 💘",
            f"Рады приветствовать! {user.username}, чувствуй себя как дома. ✨",
            f"Приветик! {user.username}, мы как раз тебя ждали! ☕",
            f"Добро пожаловать, {user.username}! Пусть этот вечер будет особенным! 🌟"
        ]
        
        # Ждем 2 секунды, чтобы человек успел зайти и увидеть чат
        await asyncio.sleep(2)
        await self.highrise.chat(random.choice(greetings))

if __name__ == "__main__":
    # ДАННЫЕ ДЛЯ ЭТОГО БОТА
    room_id = "69ee35fab6bcfa4b70966bac"
    token = "93356fc362c144b1364b9b56314cd27400ad3d7737a7eeff88758290dbbae28d"
    
    asyncio.run(main(WelcomeBot(), room_id, token))
