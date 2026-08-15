import os
import json
import asyncio
import random
from highrise import BaseBot, __main__, User
from highrise.models import SessionMetadata, Position
from highrise.__main__ import BotDefinition

ROOM_ID = "6851d25724cd01791ef3c7e2"
TOKEN = "e50f2af5a9d261b76c044f7a1673563c2bfad96012d0bfe1ed9d4d267930e5f3"
POS_FILE = "bartender_pos.json"

DRINKS = ["Коктейль «Highrise»", "Холодный лимонад", "Горячий шоколад", "Эспрессо", "Мохито", "Сок"]

class BartenderBot(BaseBot):
    def __init__(self):
        super().__init__()
        self.saved_position = self.load_position()

    def load_position(self):
        if os.path.exists(POS_FILE):
            try:
                with open(POS_FILE, "r") as f:
                    data = json.load(f)
                    return Position(data["x"], data["y"], data["z"], data.get("facing", "FrontRight"))
            except Exception as e:
                print(f"Ошибка чтения позиции: {e}")
        return None

    async def on_start(self, session_metadata: SessionMetadata):
        print("Бармен вышел на смену!")
        if self.saved_position:
            await asyncio.sleep(3)
            try:
                await self.highrise.walk_to(self.saved_position)
            except Exception as e:
                print(f"Ошибка перемещения: {e}")

    async def on_chat(self, user: User, message: str) -> None:
        try:
            text = message.lower().strip()

            # Установка позиции за стойкой
            if text in ["!bartenderpos", "!бармен"]:
                room_users = await self.highrise.get_room_users()
                for room_user, pos in room_users.content:
                    if room_user.id == user.id and isinstance(pos, Position):
                        with open(POS_FILE, "w") as f:
                            json.dump({"x": pos.x, "y": pos.y, "z": pos.z, "facing": pos.facing}, f)
                        self.saved_position = pos
                        await self.highrise.walk_to(pos)
                        await self.highrise.chat(f"Готово, @{user.username}! Теперь я за стойкой. 🍸")
                        break

            # Показать меню
            elif text == "!menu":
                drinks_list = ", ".join(DRINKS)
                await self.highrise.chat(f"Привет, @{user.username}! У нас есть: {drinks_list}.")

            # Налить случайный напиток
            elif text in ["!налей", "!заказ", "налей"]:
                drink = random.choice(DRINKS)
                await self.highrise.chat(f"Держи, @{user.username}! Твой {drink}. Приятного отдыха! 🍹")

        except Exception as e:
            print(f"Ошибка чата: {e}")

if __name__ == "__main__":
    definitions = [BotDefinition(BartenderBot(), ROOM_ID, TOKEN)]
    asyncio.run(__main__.main(definitions))
