import orjson
import aiohttp
import pprint
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

        if DEBUG:
            sprint(f"Messager.run AMQP_URI={AMQP_URI}", c="green")       

        for catched_message in catch(queue="alerts", uri=AMQP_URI, count=50):

            if DEBUG:
                sprint(f"Messager.run catched_message={catched_message}", c="green")    

            await self.send_telegram_alert(catched_message)

    async def send_telegram_alert(self, message):

        if DEBUG:
            sprint(f"Messager.send_telegram_alert -> {message}", c="green")        

        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

        for chat_id in TELEGRAM_CHAT_IDS:
            attempts = 5
            params = {
                "chat_id": chat_id,
                "text": pprint.pformat(message),
            }

            while attempts >= 0:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, params=params) as resp:
                        if resp.status == 200:
                            return
                        elif resp.status == 429:
                            attempts -= 1
                            await asyncio.sleep(throttle_delay)
                            continue
                        else:
                            raise RuntimeError(f"Bad HTTP response: {resp}")

