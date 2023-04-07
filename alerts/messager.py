import orjson
import aiohttp
from simple_print import sprint
from throw_catch import catch
from settings import DEBUG
from settings import AMQP_URI
from settings import TELEGRAM_BOT_TOKEN
from settings import TELEGRAM_CHAT_IDS


class Messager:
    def __init__(self, data={}):
        self.data = data

    async def run(self):
        for catched_message in catch(tag="alerts", uri=AMQP_URI, count=50):
            await self.__send_telegram_alert(catched_message)

    async def __send_telegram_alert(self, message):

        text = orjson.dumps(message)
        image_path = message["payload"].get("image_path") 

        if DEBUG:
            sprint(f"Messager -> _send_to_telegram telegram_chat_id={chat_id} text={text}", c="cyan")

        if image_path:
            telegram_api_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto?chat_id=@{chat_id}&photo={image_path}&caption={text}&parse_mode=markdown"
        else:
            telegram_api_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage?chat_id=@{chat_id}&text={text}&parse_mode=markdown&disable_web_page_preview=true"

        async with aiohttp.ClientSession() as session:
            async for chat_id in TELEGRAM_CHAT_IDS:
                hops = 1
                while hops <= 3:
                    async with session.post(telegram_api_url, json={"chat_id": chat_id, "text": text}) as res:
                        data = await res.json()
                        
                        if DEBUG:
                            sprint(f"Result: {data}", c="green", s=1, p=1)
                      
                        if data.get("ok"):
                            break

                        hops += 1
