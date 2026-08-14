import os
import asyncio
from highrise import BaseBot, __main__
from highrise.models import SessionMetadata, User, Position

# Полная база танцев (1 - 150)
EMOTE_MAP = {
    "1": "idle-dance-casual", "2": "dance-single-1", "3": "dance-single-2", "4": "dance-shoppingcart", 
    "5": "dance-russian", "6": "dance-macarena", "7": "dance-weird", "8": "dance-tiktok2", 
    "9": "dance-tiktok8", "10": "dance-blackpink", "11": "dance-pennypacker", "12": "dance-metal", 
    "13": "dance-floss", "14": "dance-duckwalk", "15": "dance-breakdance", "16": "dance-orangejustice", 
    "17": "dance-sicko", "18": "dance-smoothwalk", "19": "dance-vogueing", "20": "dance-zombie",
    "21": "dance-gangnam", "22": "dance-handsup", "23": "dance-aerobics", "24": "dance-frog", 
    "25": "dance-bunnyhop", "26": "dance-techno", "27": "dance-disco", "28": "dance-samba", 
    "29": "dance-salsa", "30": "dance-twerk", "31": "dance-belly", "32": "dance-tap", 
    "33": "dance-hiphop", "34": "dance-kpop", "35": "dance-robot", "36": "dance-shuffle", 
    "37": "dance-rock", "38": "dance-swing", "39": "dance-waltz", "40": "dance-chacha",
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
    "89": "emote-dodge", "90": "emote-victory", "91": "emote-defeat", "92": "emote-taunt", 
    "93": "emote-cheer", "94": "emote-salute", "95": "emote-pray", "96": "emote-meditate", 
    "97": "emote-yoga", "98": "emote-stretch", "99": "emote-warmup", "100": "emote-cooldown",
    "101": "dance-tiktok1", "102": "dance-tiktok3", "103": "dance-tiktok4", "104": "dance-tiktok5",
    "105": "dance-tiktok6", "106": "dance-tiktok7", "107": "dance-tiktok9", "108": "dance-tiktok10",
    "109": "dance-weird1", "110": "dance-weird2", "111": "dance-weird3", "112": "dance-weird4",
    "113": "dance-single3", "114": "dance-single4", "115": "dance-single5", "116": "dance-single6",
    "117": "emote-pose1", "118": "emote-pose2", "119": "emote-pose3", "120": "emote-pose4",
    "121": "emote-pose5", "122": "emote-pose6", "123": "emote-pose7", "124": "emote-pose8",
    "125": "emote-fashion", "126": "emote-model", "127": "emote-strut", "128": "emote-runway",
    "129": "emote-spin", "130": "emote-twirl", "131": "emote-drop", "132": "emote-pop",
    "133": "emote-lock", "134": "emote-wave1", "135": "emote-wave2", "136": "emote-groove",
    "137": "emote-bounce", "138": "emote-sway", "139": "emote-shake", "140": "emote-shimmy",
    "141": "dance-party", "142": "dance-club", "143": "dance-rave", "144": "dance-disco1",
    "145": "dance-disco2", "146": "dance-retro", "147": "dance-vintage", "148": "dance-classic",
    "149": "dance-modern", "150": "dance-freestyle"
}

class DanceBot(BaseBot):
    async def on_start(self, session_metadata: SessionMetadata) -> None:
        print("Дэнс-бот запущен!")

    async def on_chat(self, user: User, message: str) -> None:
        text = message.strip()
        if text in EMOTE_MAP:
            await self.highrise.send_emote(EMOTE_MAP[text], user.id)

if __name__ == "__main__":
    room_id = os.getenv("ROOM_ID")
    token = os.getenv("BOT_TOKEN")
    definitions = [__main__.BotDefinition(DanceBot(), room_id, token)]
    asyncio.run(__main__.main(definitions))
